from .src.admins import admins
from box import Box
import json

info=Box(json.load(open(f'{__path__[0]}/main.json', 'r')))

async def init(app,m,me,args) -> None:
  await admins(app,m,me,args)
