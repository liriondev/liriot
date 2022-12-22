import sqlite3,inspect,json,os,jinja2
from datetime import datetime as dt
from box import Box

class utils:
	try:config=Box(json.load(open('settings.json','r'))+Box({'version': '0.2-stable'}))
	except:pass
	me=None

def templates(modname, app):
	my_loader = jinja2.ChoiceLoader([
		app.jinja_loader,
		jinja2.FileSystemLoader([
			f"{os.getcwd()}/modules/{modname}/templates"]),
		])
	app.jinja_loader = my_loader

def language(func):
	async def wrapper(app,m,me,args):
		tmp=Box(json.load(open(f'modules/{func.__name__}/language.json','r')))
		language=tmp[utils.config.language]
		await func(app,m,me,args,language)
	return wrapper

class Logs():
	def __init__(self) -> None:
		self.db=DataBase('logs')
		self.db.create([i[1] for i in inspect.stack() if '<frozen' not in i[1]][1].split('/')[-1:][0][:-3], (
			self.db.Column('type'),
			self.db.Column('msg'),
			self.db.Column('time')
		))
	
	def add(self,type:str,msg:str) -> None:
		msg=msg.replace('"','#2#')
		self.db.insert([i[1] for i in inspect.stack() if '<frozen' not in i[1]][1].split('/')[-1:][0][:-3], 'type,msg,time', f'"{type}","{msg}","{dt.now().strftime("%m.%d.%Y, %H:%M:%S")}"')
	
	def view(self,md=False) -> dict:
		if not md:
			all_logs=self.db.select('sqlite_master', 'name', 'type="table"')
			return all_logs
		else: return self.db.select(md, '*')

class DataBase(object):
	def __init__(self, name:str=False) -> None:
		try:os.mkdir('databases/')
		except:pass
		if not name:self.db_name=f"databases/{[i[1] for i in inspect.stack() if '<frozen' not in i[1]][1].split('/')[-1:][0][:-3]}.db"
		else:self.db_name=f"databases/{name}.db"
		
	def create(self, table_name:str, columns):
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(str(x) for x in columns)})')
		conn.commit()
		cursor.close()
		
	def insert(self, table_name:str, column_name:str, column_value:str) -> None:
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(f'INSERT INTO {table_name} ({column_name}) VALUES ({column_value})')
		conn.commit()
		cursor.close()
	
	def update(self, table_name:str, values:str, where:str='') -> None:
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(f'UPDATE {table_name} SET {values} {"" if not len(where) else "WHERE "+where}')
		conn.commit()
		cursor.close()
	
	def select(self, table_name:str, column:str, where:str='') -> Box:
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(f'SELECT {column} FROM {table_name} {"" if not len(where) else "WHERE "+where}')
		coln=[i[0] for i in cursor.description]
		data=cursor.fetchall()
		res={}
		for i in range(len(data)):
			res[i]=dict.fromkeys(coln)
			for y in range(len(coln)):
				res[i][coln[y]]=data[i][y]
		return Box(res)
		
	def Column(self, column_name:str, column_value_type:str='INTEGER', primary_key:bool=False) -> str:
		return f'{column_name} {column_value_type} {"PRIMARY KEY" if primary_key else ""}'
		
	def Where(self, column_name:str, column_value:str) -> str:
		return f'{column_name}="{column_value}"'