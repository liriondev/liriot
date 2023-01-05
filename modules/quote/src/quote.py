from core.utils import language
import requests, json, base64
from io import BytesIO
from PIL import Image

@language
async def quote(app,m,me,args,language):
    avatar = await app.download_media([i async for i in app.get_chat_photos(m.reply_to_message.from_user.id)][0].file_id, in_memory=True)
    url = "https://quotes.fl1yd.su/generate"
    avatar = base64.b64encode(avatar.getvalue()).decode()
    params = json.dumps({
        "messages": [
          {
               "text": "really",
               "author": {"id": m.reply_to_message.from_user.id,"name": f"{m.reply_to_message.from_user.first_name} {m.reply_to_message.from_user.last_name}","avatar":avatar},
               "reply": {}
           }
        ],
        "quote_color": "#162330",
        "text_color": "#fff",
    }, ensure_ascii=False)

    response = requests.post(
        url, 
        data=params.encode("utf-8"),
        headers={'Content-Type': 'application/json; charset=UTF-8'},
    )

    tmp = BytesIO()
    tmp.name = "test"

    quote = BytesIO(response.content)
    quote.name = "test"

    image = Image.open(quote)
    image.save(tmp, format="webp")

    await app.send_sticker(m.chat.id, tmp, reply_to_message_id=m.reply_to_message.id)