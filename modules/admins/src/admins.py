from core.utils import language
from time import time
from pyrogram.types import ChatPermissions

@language
async def admins(app,m,me,args,language):
	
	if args[0][1:]=='ban':
		
		if len(args)==2:
			try:
				await app.ban_chat_member(m.chat.id, args[1])
				return await m.edit(language.banned)
			except: return await m.edit(language.failed_ban)
			
		else:
			try:
				await app.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
				return await m.edit(language.banned)
			except: return await m.edit(language.failed_ban)
			
	if args[0][1:]=='kick':
		
		if len(args)==2:
			try:
				await app.ban_chat_member(m.chat.id, args[1])
				await app.ban_chat_member(m.chat.id, args[1])
				return await m.edit(language.banned)
			except: return await m.edit(language.failed_ban)
			
		else:
			try:
				await app.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
				await app.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
				return await m.edit(language.kicked)
			except: return await m.edit(language.failed_kick)
			
	if args[0][1:]=='mute':
		
		if len(args)==2:
			try:
				time_mute = int(time()+{'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[args[1][-1:]]*args[1][:-1])
				await app.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, ChatPermissions(), time_mute)
				return await m.edit(language.muted)
			except: return await m.edit(language.failed_mute)
			
		else:
			try:
				await app.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, ChatPermissions())
				return await m.edit(language.muted)
			except: return await m.edit(language.failed_mute)
			