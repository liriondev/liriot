from core.utils import language
from core.loader import loader

async def modules_daemon(app, me):
	for mod in loader.list():
			if loader.load(mod).info.load_event=='background':
				await loader.load(mod).init(app,me)
