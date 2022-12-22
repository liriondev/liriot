from pyrogram import Client
from core.loader import loader
from core.utils import Logs

def starting():
	log=Logs()
	try:log.view('background_system')[list(log.view('main'))[-1]].msg;return True
	except:log.add('info', 'BG system start finished');return False

@Client.on_raw_update(group=1)
async def handler(app,handler,raw,_):
	if not starting():
		for mod in loader.list():
			if loader.load(mod).info.load_event=='background':
				await loader.load(mod).init(app)
	for mod in loader.list():
		if loader.load(mod).info.load_event=='all':
			await loader.load(mod).init(app,handler,raw)
	