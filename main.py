import os, hashlib, json, sys, asyncio
from box import Box
from flask import Flask, render_template, redirect, url_for, request, make_response
from threading import Thread
from core.utils import DataBase
from tabulate import tabulate
from waitress import serve

web = Flask(__name__)
web.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db=DataBase()
if not os.path.exists('databases/main.db'):
	db.create('info', (db.Column('logo'),))

def check_cookies(request):
	try:
		if utils.config.password==request.cookies.get('token'): return True
	except Exception as e: print(e)
	return redirect('/')

@web.route("/")
def index():
	if os.path.isfile('settings.json'): return render_template("auth.html")
	else: return render_template("setup.html")

@web.route("/create")
def auth():
	with open("settings.json", "w") as f:
		f.write(json.dumps({
			"api_id": request.args.get('api_id'),
			"api_hash": request.args.get('api_hash'),
			"language": request.args.get('language'),
			"password": request.args.get('password')
		}))
		f.close()
	resp = make_response("Succesfull")
	resp.set_cookie('token', request.args.get('password'))
	return resp

@web.route("/login")
def login():
	if request.args.get('password')==utils.config.password:
		resp = make_response("Succesfull")
		resp.set_cookie('token', request.args.get('password'))
	else: resp='Wrong password.'
	
	return resp

@web.route("/exec")
def execute():
	if check_cookies(request): return 'ok' if eval(request.args.get('command')) else 'error'

@web.route("/home")
def home():
	if check_cookies(request): return render_template('home.html')
	else: return redirect('/');

@web.route("/modules")
def modules():
	if check_cookies(request): return render_template('list.html', types='modules')

@web.route("/get")
def preloading():
	if check_cookies(request):
		if request.args.get('data')=='home_preloader':
			if not utils.me: utils.me=app.get_me()
			photo=app.get_profile_photos("me")
			if photo:
				tmp=db.select('info', 'logo')[list(db.select('info', 'logo'))[-1]].logo if db.select('info', 'logo') else None
				if photo[-1].file_unique_id!=tmp:
					app.download_media(app.get_profile_photos("me", limit=1)[0].file_id, file_name="static/img/ava.png")
					db.insert('info', 'logo', f'{photo[-1].file_unique_id}')
				ava=True
			else: ava=False
			data=Box({
				'version': sys.version.split(' ')[0],
				'cpu': int(psutil.cpu_percent(4)),
				'disk': int(psutil.disk_usage('/').percent),
				'os': os.uname().sysname,
				'arch': os.uname().machine,
				'user': app.send(functions.users.GetFullUser(id=app.resolve_peer(utils.me.id))),
				'avatar': 'ava' if ava else 'logo'
			})
			tmp=open('templates/home_load.html', 'r').read()
			return tmp.format(data=data)
		if request.args.get('data')=='modules':
			out='<div class="modules">\n'
			tmp=open('templates/list_mod.html', 'r').read()
			i=0
			for mod in loader.list():
				out+=tmp.format(mod=loader.load(mod).info, help_=loader.load(mod).info.module_help.replace('\n', '<br>'), commands=', '.join(loader.load(mod).info.module_commands), raw_name=mod, index=i)
				i+=1
			out+=f'</div>\n<script>for(let i=0;i<{i};i++){{$("#info-"+i).css("height","40px")}}'
			return out

@web.after_request
def add_header(r):
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r 

if os.path.isfile('settings.json'):
	from pyrogram import Client, filters
	from pyrogram.raw import functions
	from core.loader import loader
	from core.utils import utils
	import asyncio, time, traceback, psutil

	app = Client('LiteBot', api_id=utils.config.api_id, api_hash=utils.config.api_hash)

	@app.on_message(filters.text)
	async def main(client, m) -> None:
		
		if not utils.me:
			utils.me=await app.get_me()
			await loader.load('modules_daemon').init(app,utils.me)
			
		args=m.text.split(' ') if len(m.text.split(' ')) > 0 else [m.text, ' ']
		
		for mod in loader.list():
			
			if loader.load(mod).info.public and m.from_user.id == me.id:
				if args[0][1:] in loader.load(mod).info.module_commands and loader.load(mod).info.load_event=='msg':
					await loader.load(mod).init(app,m,utils.me,args)
					break

			else:
				if args[0][1:] in loader.load(mod).info.module_commands and loader.load(mod).info.load_event=='msg':
					await loader.load(mod).init(app,m,utils.me,args)
					break

	if __name__=='__main__':
		print(tabulate([["liri0t", "Addres web panel", "Modules"], ["v-0.1-beta", "127.0.0.1:5000", len(loader.list())]], tablefmt="grid"))
		Thread(target=serve, args=(web,), kwargs={'host': '0.0.0.0', 'port': 5000}, daemon=True).start()
		app.run()
		
else:
	print(tabulate([["liri0t", "Addres web panel", "Modules"], ["v-0.1-beta", "127.0.0.1:5000", len(loader.list())]], tablefmt="grid"))
	serve(web, host='0.0.0.0')