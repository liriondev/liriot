from core.utils import utils, language
from io import StringIO
from meval import meval
import sys, traceback, asyncio

@language
async def python(app,m,me,args,language):
  if args[0]=='.eval':
    try:
      old_stdout = sys.stdout 
      sys.stdout = mystdout = StringIO()
      await meval(' '.join(args[1:]), globals(), app=app, m=m, reply=m.reply_to_message, me=me)
      sys.stdout = old_stdout
      await m.edit(f'''
**Code:**

```{' '.join(args[1:])}```

**Result:**

```{mystdout.getvalue()}```
            ''')
    except:
      sys.stdout = old_stdout
      await m.edit(f'''
**Code:**

```{' '.join(args[1:])}```

**Traceback:**

```{traceback.format_exc()}```
            ''')
  if args[0]=='.math':
    reply=m.reply_to_message
    try: tmp=eval(' '.join(args[1:]), locals())
    except Exception as tmp: pass
    await m.edit(f'''**Example:**\n\n{' '.join(args[1:])}\n\n**Output:**\n\n{tmp}''')