import asyncio

import uvloop
import yaml
from loguru import logger
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.methods.utilities.compose import compose

from telegram_pipe.clients import initialize_clients
from telegram_pipe.config import (
    PIPELINES_FILEPATH,
)
from telegram_pipe.filters import available_filters
from telegram_pipe.pipeline import Pipeline

# Get the pipelines from the yaml file
with open(PIPELINES_FILEPATH) as f:
    pipelines_list = yaml.safe_load(f)['pipelines']


async def main() -> None:
    uvloop.install()

    available_clients = await initialize_clients()

    pipelines: list[Pipeline] = []

    for pipeline in pipelines_list:
        filters_ = [
            available_filters[filter_name]
            for filter_name in pipeline['filters']
        ]
        try:
            sender = available_clients[pipeline['sender']]
        except KeyError:
            sender = available_clients['me']
            logger.warning(
                'Sender not found, using "me" instead',
            )
        try:
            listener = available_clients[pipeline['listener']]
        except KeyError:
            listener = available_clients['me']
            logger.warning(
                'Listener not found, using "me" instead',
            )
        try:
            use_listener_on_fail = pipeline['use_listener_on_fail']
        except KeyError:
            use_listener_on_fail = True
            logger.warning(
                'use_listener_on_fail not found, using "False" instead',
            )

        pipelines.append(
            Pipeline(
                sources=pipeline['sources'],
                destinations=pipeline['destinations'],
                filters=filters_,
                sender=sender,
                listener=listener,
                use_listener_on_fail=use_listener_on_fail,
            )
        )

    # Add the handlers for each pipeline
    for pipeline in pipelines:
        logger.info(
            'Adding handler for pipeline {pipeline}', pipeline=pipeline
        )
        pipeline.listener.add_handler(
            MessageHandler(
                pipeline.get_handler(), filters=pipeline.get_filter()
            )
        )
    await compose(list(available_clients.values()))


logger.info('Running app...')
asyncio.run(main())
