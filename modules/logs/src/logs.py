from core.loader import loader
from core.utils import Logs

async def logs(app,m,me,args):
	log=Logs()
	log_=[log.view()[l]['name'] for l in log.view()]
	if len(args)==1:await m.edit('List logs: `'+", ".join(log_)+'`')
	else:
		try:
			log2=log.view(args[1])[list(log.view(args[1]))[-1]]
			log2.msg=log2.msg.replace("#2#", '"')
			await m.edit(f'**Log `{args[1]}` file:**\n**Type:** {log2.type}\n\n**Message:** `{log2.msg}`')
		except: await m.edit(f'**Log `{args[1]}` file:**\n\n**~clear~**')