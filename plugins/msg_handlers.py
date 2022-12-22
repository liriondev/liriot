from pyrogram import filters, Client
import pyrogram
from pyrogram.raw import functions
from core.loader import loader
from plugins.filters.command import start_msg
from core.utils import utils, DataBase

@Client.on_message(start_msg('.'))
async def main(app, m) -> None:
	
	if not utils.me:utils.me=await app.get_me()

	args=m.text.split(' ') if len(m.text.split(' ')) > 0 else [m.text, ' ']
	
	for mod in loader.list():
		
		if loader.load(mod).info.public:
			if args[0][1:] in loader.load(mod).info.module_commands and loader.load(mod).info.load_event=='msg':
				try:await loader.load(mod).init(app,m,utils.me,args)
				except: await m.edit(f'**Error, view logs "```.logs loader```"**')
				break
		elif utils.me.id == m.from_user.id:
			if args[0][1:] in loader.load(mod).info.module_commands and loader.load(mod).info.load_event=='msg':
				await loader.load(mod).init(app,m,utils.me,args)
				#except Exception as e: await m.edit(f'**Error, view logs "```.logs loader```"**');print(e)
				break