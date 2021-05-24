import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AK = os.environ.get("API_KEY")
GAC = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
BN = os.environ.get("BUCKET_NAME")