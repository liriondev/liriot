import io
from core.utils import language
from pygments.formatters import JpgImageFormatter
from pygments import highlight
from pygments import lexers
from pygments.style import Style
from PIL import Image, ImageDraw, ImageFilter
from pygments.token import Token, Comment, Keyword, Name, String, \
     Error, Generic, Number, Operator

def code_block(code, language, style='dracula', font_size=50, line_numbers =True):
	
	fmt = JpgImageFormatter(style=style, font_size=font_size, line_numbers=line_numbers, line_number_bg=(40, 42, 54), line_number_fg =(100, 100, 100))
													
	lex = lexers.get_lexer_by_name(language)
	code = Image.open(io.BytesIO(highlight(code, lex,fmt)))
	
	center=int((code.size[0]+300-code.size[0]-25)/2), int((code.size[1]+300-code.size[1]-95)/2)
	
	img = Image.new('RGB', (code.size[0]+300, code.size[1]+300), (175,238,238))
	# bg=Image.open('modules/dev_module/src/bg.jpg').resize(img.size)
	# img.paste(bg)
	idraw = ImageDraw.Draw(img)
	
	idraw.rounded_rectangle( ( center, (code.size[0]+70+center[0], code.size[1]+120+center[1]) ), 20, fill=(40, 42, 54) )
	
	img.paste(code, (center[0]+20, center[1]+75))
	
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
		try:await app.send_document(m.chat.id, code_block(m.reply_to_message.text, args[1], line_numbers=False), reply_to_message_id=m.reply_to_message.id)
		except:await app.send_document(m.chat.id, code_block(m.text.replace(f'{args[0]} {args[1]}',''), args[1], line_numbers=False), reply_to_message_id=m.reply_to_message.id)
		await m.delete()
	else:
		await m.edit('**Generation...**')
		await app.send_document(m.chat.id, code_block(m.text.replace(f'{args[0]} {args[1]}', ''), args[1], line_numbers=False))
		await m.delete()
