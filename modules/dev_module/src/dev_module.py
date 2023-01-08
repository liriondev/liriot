import io
from core.utils import language
from pygments.formatters import JpgImageFormatter
from pygments import highlight
from pygments import lexers
from PIL import Image, ImageDraw, ImageFilter


def code_block(code, language, style='dracula', font_size=50, line_numbers =True):
	
	fmt = JpgImageFormatter(style=style, font_size=font_size, line_numbers=line_numbers, line_number_bg=(40, 42, 54), line_number_fg =(100, 100, 100))
													
	lex = lexers.get_lexer_by_name(language)
	code = Image.open(io.BytesIO(highlight(code, lex,fmt)))
	
	center=int((code.size[0]+500-code.size[0]-10)/2), int((code.size[1]+800-code.size[1]-70)/2)
	
	img = Image.new('RGBA', (code.size[0]+500, code.size[1]+800))
	bg=Image.open('modules/dev_module/src/bg.jpg').resize(img.size)
	img.paste(bg.filter(ImageFilter.BoxBlur(2)))
	idraw = ImageDraw.Draw(img)
	
	idraw.rounded_rectangle( ( center, (code.size[0]+40+center[0], code.size[1]+90+center[1]) ), 20, fill=(40, 42, 54) )
	
	img.paste(code, (center[0]+5, center[1]+60))
	
	idraw.rounded_rectangle( ( (center[0]+15, center[1]+15), (center[0]+47, 47+center[1]) ), 100, fill=(255, 85, 85) )
	idraw.rounded_rectangle( ( (center[0]+62, center[1]+15), (center[0]+94, 47+center[1]) ), 100, fill=(241, 250, 140) )
	idraw.rounded_rectangle( ( (center[0]+109, center[1]+15), (center[0]+141, 47+center[1]) ), 100, fill=(80, 250, 123) )
	
	tmp = io.BytesIO()
	tmp.name = 'code.png'

	img.save(tmp, format='PNG')

	return tmp

@language 
async def dev_module(app,m,me,args,language):
	
	if m.reply:
		await m.edit('**Generation...**')
		await app.send_document(m.chat.id, code_block(m.reply_to_message.text, args[1]), reply_to_message=m.reply_to_message.id)
		await m.delete()
	else:
		await m.edit('**Generation...**')
		try: await app.send_document(m.chat.id, code_block(m.text.replace(f'{args[0]} {args[1]}'), args[1]), reply_to_message=m.reply_to_message.id)
		except: await m.delete();await app.send_document(m.chat.id, code_block(m.text.replace(f'{args[0]} {args[1]}'), args[1]))