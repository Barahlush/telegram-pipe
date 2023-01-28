import os

import dotenv

dotenv.load_dotenv()
API_ID = os.getenv('API_ID', '')
API_HASH = os.getenv('API_HASH', '')
if not API_HASH or not API_ID:
    raise ValueError('API_ID and API_HASH must be set')

PIPELINES_FILEPATH = 'pipelines.yaml'
