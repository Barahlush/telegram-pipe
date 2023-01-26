from typing import Any

from pyrogram import filters
from pyrogram.client import Client


def word_lookup_filter(
    positive: str | list[str], negative: str | list[str]
) -> filters.Filter:
    """Filter messages that contain a word from a list of positive words and
    don't contain a word from a list of negative words.
    """
    if isinstance(positive, str):
        positive = [positive]
    if isinstance(negative, str):
        negative = [negative]

    async def func(_: filters.Filter, __: Client, message: Any) -> bool:
        if not message.text:
            return False
        text = message.text.lower()
        return all(word in text for word in positive) and not any(
            word in text for word in negative
        )

    return filters.create(func)


pipeline_filters = {
    'job_filter': word_lookup_filter('python', 'senior'),
}
