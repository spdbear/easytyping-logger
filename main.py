import sys
import pyocr
import pyocr.builders

import cv2
from PIL import Image


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
        Image.open(src),
        builder=pyocr.builders.DigitBuilder(tesseract_layout=6)
    )
    return dst


if __name__ == "__main__":
    img_path = "./img/img99091090014.jpg"
    out = imageToText(img_path)
    img = cv2.imread(img_path)
    print(out)
