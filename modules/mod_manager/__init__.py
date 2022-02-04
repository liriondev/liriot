from .src.mod_manager import mod_manager
from box import Box
import json

info=Box(json.load(open(f'{__path__[0]}/main.json', 'r')))

async def init(app,m,me,args) -> None:
  await mod_manager(app,m,me,args)
