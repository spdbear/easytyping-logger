# -*- coding: utf-8 -*-
from oauth2client.service_account import ServiceAccountCredentials
import sys
import pyocr
import pyocr.builders

from PIL import Image
import os
import datetime

import gspread
import re
import glob

import getenv

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


class ChangeHandler(FileSystemEventHandler):

    def on_created(self, event):
        # img_path = event.src_path を使うと
        # ダウンロード一時ファイルが得られてしまうので
        # 力技でファイルを取得する
        time.sleep(1)
        list_of_files = glob.glob(getenv.TARGET_DIR+"/*")
        img_path = max(list_of_files, key=os.path.getctime)
        log_downloaded_image(img_path)


def get_sheet():
    # ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。

    # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # 認証情報設定
    # ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        getenv.CREDENTIAL_JSON_PATH, scope)

    # OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)
    # 共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    getenv.SPREADSHEET_KEY = '1k9V8Cj8_5WwNn39ylnkIv4GVXlw-bJ-Pmy9x-xPAW8k'

    # 共有設定したスプレッドシートのシート1を開く
    wks = gc.open_by_key(getenv.SPREADSHEET_KEY).sheet1

    return wks


def write_sheet(data):
    header = list(data.keys())
    latest = list(data.values())
    sheet = get_sheet()
    sheet.append_row(latest)
    print(f"Uploaded: {data}")


def image_to_text(src):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)

    tool = tools[0]
    dst = tool.image_to_string(
        src,
        builder=pyocr.builders.DigitBuilder(tesseract_layout=6)
    )
    return dst


def ocr_from_image(img_path):
    img = Image.open(img_path).convert("L").point(
        lambda x: 0 if x < 192 else 255, mode="1")
    crops = {"types": (281, 145, 332, 172),
             "time_m": (251, 194, 273, 223),
             "time_s": (297, 195, 331, 222),
             "speed": (271, 245, 333, 273),
             "misstypes": (297, 295, 333, 322),
             }
    ocr_result = {}
    for k, v in crops.items():
        out = image_to_text(img.crop(v))
        # img.crop(v).save(f"{k}_{os.path.basename(img_path)}")
        ocr_result[k] = out

    return ocr_result


def ocr_image(img_path):
    ocr_result = ocr_from_image(img_path)
    output = {}
    output["date"] = datetime.datetime.fromtimestamp(
        os.stat(img_path).st_atime).strftime("%Y/%m/%d %H:%M:%S")
    output["types"] = int(ocr_result["types"])
    output["time"] = int(ocr_result["time_m"]) * 60 + int(ocr_result["time_s"])
    output["misstypes"] = int(ocr_result["misstypes"])
    output["speed"] = float(ocr_result["speed"])
    output["missrate"] = int(ocr_result["misstypes"]) / \
        int(ocr_result["types"])
    return output


def log_downloaded_image(img_path):
    m = re.search(r'img[0-9]{11,12}.jpg$', img_path)

    if(m == None):
        print("this is not typing result")
    else:
        typing_data = ocr_image(img_path)
        write_sheet(typing_data)


def watch_directory():
    print(f"Monitoring directory {getenv.TARGET_DIR} ...")
    while 1:
        event_handler = ChangeHandler()
        observer = Observer()
        observer.schedule(event_handler, getenv.TARGET_DIR, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    watch_directory()
