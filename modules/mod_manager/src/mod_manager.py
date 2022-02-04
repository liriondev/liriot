from core.utils import language
from core.loader import loader

@language
async def mod_manager(app,m,me,args,language):
  if args[0]=='.list':
    out=''
    for mod in loader.list():
      module=loader.load(mod).info
      out+=f'\n**{module.module_name}** (```{mod}```): {", ".join(module.module_commands)}'
    await m.edit(language.mod_list+'\n'+out)
  if args[0]=='.reload':
    for mod in loader.list():
      loader.reload(mod)
    await m.edit(language.reload)
  