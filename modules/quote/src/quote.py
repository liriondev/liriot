from core.utils import language
from PIL import Image, ImageDraw, ImageFont
import os

def wrap_text(text, font):
    text_lines = []
    text_line = []
    text = text.replace('\n', ' [br] ')
    words = text.split()
    font_size = font.getsize(text)
    for word in words:
        if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue
        text_line.append(word)
        w, h = font.getsize(' '.join(text_line))
        if w > 600:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]
    if len(text_line) > 0:
        text_lines.append(' '.join(text_line))
    return '\n'.join(text_lines)
    
def prepare_mask(size, antialias = 2):
    mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
    return mask.resize(size, Image.ANTIALIAS)

def crop(im, s):
    w, h = im.size
    k = w / s[0] - h / s[1]
    if k > 0: im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
    elif k < 0: im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
    return im.resize(s, Image.ANTIALIAS)

def msg_box(name, msg):
	font_msg = ImageFont.truetype("modules/quote/Roboto-Bold.ttf", size=40)
	font_name = ImageFont.truetype("modules/quote/Roboto-Bold.ttf", size=50)
	size_name=130+int(font_name.getlength(name) if font_name.getlength(name)<=600 else 600)
	size_msg=130+int(font_msg.getlength(msg) if font_msg.getlength(msg)<=600 else 600)
	img = Image.new('RGBA', (size_name if size_name>size_msg else size_msg, 160+45*wrap_text(msg, font_msg).count('\n')))
	idraw = ImageDraw.Draw(img)
	idraw.rounded_rectangle( ( (0, 20), (int(size_name if size_name>size_msg else size_msg), 160+45*wrap_text(msg, font_msg).count('\n') ) ) , 30, fill=(20,20,20))
	idraw.text((40, 30), wrap_text(name, font_name), font=font_name, fill='pink' )
	idraw.text((40, 90), wrap_text(msg, font_msg), font=font_msg, fill='white')
	return img

@language 
async def quote(app,m,me,args,language):
	try:await m.delete()
	except:pass
	if len(args)==1:msg=msg_box(m.reply_to_message.from_user.first_name, m.reply_to_message.text)
	else:msg=msg_box(m.reply_to_message.from_user.first_name, ' '.join(args[1:]))
	img = Image.new('RGBA', (150+msg.size[0], msg.size[1]))
	idraw = ImageDraw.Draw(img)
	img.paste(msg, (160, 0))
	await app.download_media(m.reply_to_message.from_user.photo.big_file_id, file_name='test.png')
	im = Image.open('downloads/test.png')
	im=crop(im,(140, 140))
	im.putalpha(prepare_mask((140,140),4))
	img.paste(im, (0,20))
	img.resize((img.size[0]*2, img.size[1]*2), Image.ANTIALIAS)
	img.save('rectangle.webp', format="webp")
	await app.send_sticker(m.chat.id, 'rectangle.webp', False,  m.reply_to_message.id)
	await m.delete()
