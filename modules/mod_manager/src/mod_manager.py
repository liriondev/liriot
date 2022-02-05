import tarfile, pip, os
from core.utils import language
from core.loader import loader

@language
async def mod_manager(app,m,me,args,language):
	
	if args[0][1:]=='list':
		
		out=''
		for mod in loader.list():
			module=loader.load(mod).info
			out+=f'\n**{module.module_name}** (```{mod}```): {", ".join(module.module_commands)}'
		await m.edit(language.mod_list+'\n'+out)
		
	if args[0][1:]=='reload':
		
		loader.reload_all()
		await m.edit(language.reload)
	
	if args[0][1:]=='install':
		
		async def progress_install(current, total):
			await m.edit(f'**Downloading - {current * 100 / total:.1f}%**')
		
		if m.reply_to_message.document.file_name[-7:]=='.tar.gz':
			
			await m.reply_to_message.download(file_name='modules_tar/', progress=progress_install)
			await m.edit('**Unpacking...**')
			with tarfile.open(f'modules_tar/{m.reply_to_message.document.file_name}') as so:
				so.extractall(path='modules/')
			if os.path.exists(f'mofules/{m.reply_to_message.document.file_name[-7:]}/requirements.txt'):
				await m.edit('**Installing requirements...**')
				pip.main(['install', '-r', f'mofules/{m.reply_to_message.document.file_name[-7:]}/requirements.txt'])
			await m.edit('**Installing complete**')
		
		else: await m.edit('**No userbot archive**')