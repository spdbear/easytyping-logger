import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CREDENTIAL_JSON_PATH = os.environ.get("CREDENTIAL_JSON_PATH")
SPREADSHEET_KEY = os.environ.get("SPREADSHEET_KEY")
TARGET_DIR = os.environ.get("TARGET_DIR")
