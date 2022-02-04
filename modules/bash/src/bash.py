from core.utils import language
import os

@language
async def bash(app,m,me,args,language):
  await m.edit(f"**Code:**\n\n```{' '.join(args[1:])}```\n\n**Result:**\n\n```{os.popen(' '.join(args[1:])).read()}```")