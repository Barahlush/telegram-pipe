import uvloop
from config import API_HASH, API_ID, pipelines_list
from filters import pipeline_filters
from loguru import logger
from models import Pipeline
from pyrogram.client import Client
from pyrogram.handlers.message_handler import MessageHandler

uvloop.install()
app = Client('my_account', int(API_ID), API_HASH)

pipelines: list[Pipeline] = []

# Parse the pipelines from the pipelines.yaml file
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
