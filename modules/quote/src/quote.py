from core.utils import language
import requests, json, base64
from io import BytesIO

@language
async def quote(app,m,me,args,language):
	avatar = [i async for i in app.get_chat_photos(m.reply_to_message.from_user.id)][0].file_id
	url = "https://quotes.fl1yd.su/generate"
	params = {
        "messages": [
          {
               "text": m.reply_to_message.text,
               "author": {"id": m.reply_to_message.from_user.id,"name": m.reply_to_message.from_user.first_name,"avatar": avatar},
               "reply": {}
           }
        ],
        "quote_color": "#162330",
        "text_color": "#fff",
    }

	response = requests.post(url, json=params)

	await app.send_photo(m.chat.id, BytesIO(response.content))