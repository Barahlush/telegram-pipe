from pyrogram.client import Client

from telegram_pipe.config import API_HASH, API_ID, BOT_TOKEN


async def initialize_clients() -> dict[str, Client]:
    available_clients: dict[str, Client] = {}
    if API_HASH and API_ID:
        available_clients['me'] = Client(
            'me', api_hash=API_HASH, api_id=API_ID
        )
    if BOT_TOKEN:
        available_clients['bot'] = Client(
            'bot',
            api_hash=API_HASH,
            api_id=API_ID,
            bot_token=BOT_TOKEN,
        )
    return available_clients
