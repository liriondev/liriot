import sqlite3,inspect,json,os
from box import Box

class utils:
	config=Box(json.load(open('settings.json','r')))
	me=None

def language(func):
	async def wrapper(app,m,me,args):
		tmp=Box(json.load(open(f'modules/{func.__name__}/language.json','r')))
		language=tmp[utils.config.language]
		await func(app,m,me,args,language)
	return wrapper

class DataBase:
	def __init__(self) -> None:
		if not os.path.exists=='databases/': os.mkdir('databases/')
		self.db_name=f"databases/{[i[1] for i in inspect.stack() if '<frozen' not in i[1]][1].split('/')[-1:][0][:-3]}.db"
		
	def create(self, table_name:str, columns):
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(str(x) for x in columns)})')
		conn.commit()
		cursor.close()
		
	def insert(self, table_name:str, column_name:str, column_value:str) -> None:
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(f'INSERT INTO {table_name} ({column_name}) VALUES ("{column_value}")')
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