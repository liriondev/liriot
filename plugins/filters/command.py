from pyrogram import filters
from pyrogram.types import Message

def start_msg(data):
    async def text_filter(flt, __, m: Message) -> bool:
        try:return m.text.startswith(flt.data)
        except:return False

    return filters.create(text_filter, data=data)