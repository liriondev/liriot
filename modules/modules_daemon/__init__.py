from .src.modules_daemon import modules_daemon
from box import Box
import json

info=Box(json.load(open(f'{__path__[0]}/main.json', 'r')))

async def init(app, me) -> None:
	await modules_daemon(app, me)
