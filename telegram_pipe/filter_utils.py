from typing import ParamSpec

from pyrogram.client import Client
from pyrogram.filters import Filter
from pyrogram.types import CallbackQuery, InlineQuery, Message, Update

P = ParamSpec('P')


class CustomFilter(Filter):
    def __init__(self, *args: P.args, **kwargs: P.kwargs):
        raise NotImplementedError

    def func(self, text: str) -> bool:
        raise NotImplementedError

    async def __call__(self, _: Client, update: Update) -> bool:
        if isinstance(update, Message):
            value = str(update.text or update.caption)
        elif isinstance(update, CallbackQuery):
            value = (
                update.data
                if isinstance(update.data, str)
                else update.data.decode()
            )
        elif isinstance(update, InlineQuery):
            value = update.query
        else:
            raise ValueError(
                f"Custom filters doesn't work with {type(update)}"
            )
        return self.func(value)
