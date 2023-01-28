from dataclasses import dataclass
from functools import reduce
from operator import and_
from typing import Awaitable, Callable, Sequence, cast

from loguru import logger
from pyrogram.client import Client
from pyrogram.filters import Filter, chat
from pyrogram.types import Message


@dataclass
class Pipeline:
    """Pipeline configuration.

    Attributes:
        sources (list[str | int]): The chats from which the messages will be
            forwarded.
        destinations (list[str | int]): The chats to which the messages will be
            forwarded.
        filters (list[Filter]): The filters that will be used to select the
            messages to forward.

    """

    sources: list[str | int]
    destinations: list[str | int]
    filters: Sequence[Filter]

    def get_handler(self) -> Callable[[Client, Message], Awaitable[None]]:
        """Generate the handler for the pipeline.

        Returns:
            function: The handler for the pipeline.

        """

        async def handler(
            client: Client, message: Message  # noqa: ARG001
        ) -> None:
            logger.info(
                'Handling message "{message_text}" from "{chat_name}"',
                message_text=message.text,
                chat_name=message.chat.title,
            )
            for destination in self.destinations:
                await message.forward(destination)

        return handler

    def get_filter(self) -> Filter:
        """Generate the combined filter for the pipeline.

        Returns:
            Filter: The filter for the pipeline.

        """
        return cast(
            Filter,
            reduce(and_, self.filters) & cast(Filter, chat(self.sources)),
        )
