import sys
import pyocr
import pyocr.builders

from PIL import Image
import os
import datetime


class TypingResult:
    def __init__(self, types, time, misstypes):
        self.types = types
        self.time = time
        self.misstypes = misstypes

    def calc_misstype_rate(self):
        return self.misstypes / self.types


def write_spreadsheet():
    pass


def ocr_image(parameter_list):
    pass


def detect_downloaded_image():
    # return
    pass


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


if __name__ == "__main__":
    img_path = "./img/img99512066032.jpg"

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

    output["time"] = int(ocr_result["time_m"]) * 60 + int(ocr_result["time_s"])
    output["missrate"] = int(ocr_result["misstypes"]) / \
        int(ocr_result["types"])
    output["date"] = datetime.datetime.fromtimestamp(
        os.stat(img_path).st_atime).strftime("%Y/%m/%d %H:%M:%S")
    output["misstypes"] = ocr_result["misstypes"]
    output["types"] = ocr_result["types"]
    output["speed"] = ocr_result["speed"]
    print(output)
