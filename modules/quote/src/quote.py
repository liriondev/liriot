from core.utils import language
import requests, json, base64
from io import BytesIO

@language
async def quote(app,m,me,args,language):
    avatar = await app.download_media([i async for i in app.get_chat_photos(m.reply_to_message.from_user.id)][0].file_id, in_memory=True)
    url = "https://quotes.fl1yd.su/generate"
    avatar = base64.b64encode(avatar.getvalue()).decode()
    params = json.dumps({
        "messages": [
          {
               "text": "really",
               "author": {"id": m.reply_to_message.from_user.id,"name": m.reply_to_message.from_user.first_name,"avatar":avatar},
               "reply": {}
           }
        ],
        "quote_color": "#162330",
        "text_color": "#fff",
    }, ensure_ascii=False)

    response = requests.post(
        url, 
        json=params.encode("utf-8"),
        headers={'Content-Type': 'application/json; charset=UTF-8'},
    )

    await app.send_photo(m.chat.id, BytesIO(response.content))