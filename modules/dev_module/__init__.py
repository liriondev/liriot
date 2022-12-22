from .src.dev_module import dev_module
from box import Box
import json

info=Box(json.load(open(f'{__path__[0]}/main.json', 'r')))

async def init(app,m,me,args) -> None:
  await dev_module(app,m,me,args)
