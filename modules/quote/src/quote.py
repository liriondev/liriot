from core.utils import language
import requests, json, base64
from io import BytesIO

@language
async def quote(app,m,me,args,language):
	avatar = await app.download_media([i async for i in app.get_chat_photos(m.reply_to_message.from_user.id)][0].file_id, in_memory=True).getbuffer()
	url = "https://quotes.fl1yd.su/generate"
	params = {
        "messages": [
          {
               "text": reply.text,
               "author": {"id": reply.from_user.id,"name": reply.from_user.first_name,"avatar":base64.b64encode(bytes(avatar))},
               "reply": {}
           }
        ],
        "quote_color": "#162330",
        "text_color": "#fff",
    }

	response = requests.post(url, json=params)

	await app.send_photo(m.chat.id, BytesIO(response.content))
