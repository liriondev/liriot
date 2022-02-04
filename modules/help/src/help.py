from core.utils import utils, language
from core.loader import loader

@language
async def help(app,m,me,args,language):
  try:
    module=loader.load(args[1]).info
    msg=f'''
**{language.name}:** ```{module.module_name}```
**{language.info}:** ```{module.module_info}```

**{language.help}:**
```{module.module_help}```
            '''
    await m.edit(msg)
  except: await m.edit(language.error)