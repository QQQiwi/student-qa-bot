import os
from dotenv import load_dotenv

load_dotenv()

MODELNAME = os.environ.get("MODELNAME")
MODEL_URL = os.environ.get("MODEL_URL")