from oauth2client.service_account import ServiceAccountCredentials
import sys
import pyocr
import pyocr.builders

from dotenv import load_dotenv

from PIL import Image
import os
import datetime

import gspread
import json

import getenv


class TypingResult:
    def __init__(self, types, time, misstypes):
        self.types = types
        self.time = time
        self.misstypes = misstypes

    def calc_misstype_rate(self):
        return self.misstypes / self.types


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


def imageToText(src):
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


def ocr_image(img_path):
    img = Image.open(img_path).convert("L")
    img.point(lambda x: 0 if x < 128 else x)
    crops = {"types": (281, 145, 330, 172),
             "time_m": (251, 196, 273, 221),
             "time_s": (296, 196, 332, 221),
             "speed": (271, 245, 333, 273),
             "misstypes": (297, 295, 333, 332),
             }

    ocr_result = {}
    output = {}

    for k, v in crops.items():
        out = imageToText(img.crop(v))
        ocr_result[k] = out

    output["date"] = datetime.datetime.fromtimestamp(
        os.stat(img_path).st_atime).strftime("%Y/%m/%d %H:%M:%S")
    output["types"] = ocr_result["types"]
    output["time"] = int(ocr_result["time_m"]) * 60 + int(ocr_result["time_s"])
    output["misstypes"] = ocr_result["misstypes"]
    output["speed"] = ocr_result["speed"]
    output["missrate"] = int(ocr_result["misstypes"]) / \
        int(ocr_result["types"])
    return output


def detect_downloaded_image():
    # return
    pass


if __name__ == "__main__":
    img_path = sys.argv[1]
    typing_data = ocr_image(img_path)
    print(typing_data)
    # sheet = get_sheet()
    # cell_list = sheet.range('A1:A7')
    # print(cell_list)

    # 先頭の行に date, types, time, misstypes, speed, missrateの順に書く

    # データのある最終行を見つけてそこにデータを追加
