import uvloop
import yaml
from loguru import logger
from pyrogram.client import Client
from pyrogram.handlers.message_handler import MessageHandler

from telegram_pipe.config import API_HASH, API_ID, PIPELINES_FILEPATH
from telegram_pipe.filters import pipeline_filters
from telegram_pipe.pipeline import Pipeline

uvloop.install()
app = Client('my_account', int(API_ID), API_HASH)


# Get the pipelines from the yaml file
with open(PIPELINES_FILEPATH) as f:
    pipelines_list = yaml.safe_load(f)['pipelines']

pipelines: list[Pipeline] = []

for pipeline in pipelines_list:
    filters_ = [
        pipeline_filters[filter_name] for filter_name in pipeline['filters']
    ]
    pipelines.append(
        Pipeline(
            sources=pipeline['sources'],
            destinations=pipeline['destinations'],
            filters=filters_,
        )
    )

# Add the handlers for each pipeline
for pipeline in pipelines:
    logger.info('Adding handler for pipeline {pipeline}', pipeline=pipeline)
    app.add_handler(
        MessageHandler(pipeline.get_handler(), filters=pipeline.get_filter())
    )

logger.info('Running app...')
app.run()
