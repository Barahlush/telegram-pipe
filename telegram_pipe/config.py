import os

import dotenv
import yaml

dotenv.load_dotenv()
API_ID = os.getenv('API_ID', '')
API_HASH = os.getenv('API_HASH', '')
if not API_HASH or not API_ID:
    raise ValueError('API_ID and API_HASH must be set')

with open('pipelines.yaml') as f:
    pipelines_list = yaml.safe_load(f)['pipes']
