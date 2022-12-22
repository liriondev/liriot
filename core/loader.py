import importlib, os, sys, traceback, json
from box import Box
from core.utils import Logs

logs=Logs()

class loader:

	def list() -> dict:
		return [mod for mod in os.listdir('./modules')  if mod != "__pycache__"]
	
	def load(name:str) -> importlib:
		try:return importlib.import_module(f'modules.{name}')
		except:
			logs.add('error',traceback.format_exc())
			return Box({'info': Box(json.load(open(f'modules/{name}/main.json', 'r')))})
		
	def reload(name:str) -> None:
		for mod in os.listdir(f'modules/{name}/src/'):
			if mod != '__pycache__':
				try:
					importlib.reload(loader.load(f'{name}.src.{mod[:-3]}'))
				except:pass
		try:importlib.reload(loader.load(name))
		except Exception as e:print(e)
		
	def reload_all() -> None:
		[loader.reload(mod) for mod in loader.list()]