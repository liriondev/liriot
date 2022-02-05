import importlib, os, sys, traceback
from box import Box

class loader:
	
	def list() -> dict:
		return [mod for mod in os.listdir('./modules')  if mod != "__pycache__"]
	
	def load(name:str) -> importlib:
		mod = importlib.import_module(f'modules.{name}')
		return mod
		
	def reload(name:str) -> None:
		try: del sys.modules['modules.'+name]
		except Exception as e: print(e)
		loader.load(name)
	
	def reload_all() -> None:
		[loader.reload(mod) for mod in loader.list()]
	
	def unload(name:str) -> None:
		try: del sys.modules['modules.'+name]
		except: pass