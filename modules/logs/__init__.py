from .src.logs import logs
from core.utils import Logs
from box import Box
import json

info=Box(json.load(open(f'{__path__[0]}/main.json', 'r')))

async def init(app,m,me,args) -> None:
	await logs(app,m,me,args)

def web_panel(web):
    out=''
    log=Logs()
    logs_name=[log.view()[u].name for u in log.view()]
    logs_data={}
    template=open('modules/logs/templates/logs.html', 'r').read()
    for i in range(len(logs_name)):logs_data[i]={"name": logs_name[i], "data": log.view(logs_name[i])}
    for y in logs_data:
        log=Box(logs_data[y])
        type_=log.data[list(log.data)[-1]].type if log.data else "none"
        type_=f'''<span class="badge bgc-{type_.replace("error", "danger") if type_.replace("error", "danger") in ["danger", "warning", "succesfull", "info"] else "light"}">{type_}</span>'''
    
        out+='\n'+template.format(log=log, num=len(log.data), type_=type_)
        
    return out