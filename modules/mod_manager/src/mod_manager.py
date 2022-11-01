import tarfile, pip, os
from core.utils import language
from core.loader import loader

@language
async def mod_manager(app,m,me,args,language):
	
	if args[0][1:]=='list':
		
		out=''
		for mod in loader.list():
			module=loader.load(mod).info
			out+=f'\n╭ **{module.module_name}** (```{mod}```)\n╰> {", ".join(module.module_commands) if module.module_commands else "*none*"}\n'
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
	
	import os
	
	def is_within_directory(directory, target):
		
		abs_directory = os.path.abspath(directory)
		abs_target = os.path.abspath(target)
	
		prefix = os.path.commonprefix([abs_directory, abs_target])
		
		return prefix == abs_directory
	
	def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
	
		for member in tar.getmembers():
			member_path = os.path.join(path, member.name)
			if not is_within_directory(path, member_path):
				raise Exception("Attempted Path Traversal in Tar File")
	
		tar.extractall(path, members, numeric_owner=numeric_owner) 
		
	
	safe_extract(so, path="modules/")
			if os.path.exists(f'mofules/{m.reply_to_message.document.file_name[-7:]}/requirements.txt'):
				await m.edit('**Installing requirements...**')
				pip.main(['install', '-r', f'mofules/{m.reply_to_message.document.file_name[-7:]}/requirements.txt'])
			await m.edit('**Installing complete**')
		
		else: await m.edit('**No userbot archive**')
	
	if args[0][1:]=='share':
		try:
			if os.path.exists(f'modules_tar/{args[1]}.tar.gz'):
				await m.delete()
				await app.send_document(f'mofules_tar/{args[1]}.tar')
			else: await m.edit(language.share_not_found)
		except: await m.edit(language.share_help)