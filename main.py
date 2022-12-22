import os, hashlib, json, sys, asyncio
from box import Box
from flask import Flask, render_template, redirect, url_for, request, make_response,abort
from threading import Thread
from tabulate import tabulate
from waitress import serve

web = Flask(__name__)
web.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def auth_(func):
	if utils.config.password==request.cookies.get('token'): return func
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
	return auth_('ok' if eval(request.args.get('command')) else 'error')

@web.route("/home")
def home():
	return auth_(render_template('home.html'))

@web.route('/modules/<mod>')
def module(mod):
	if loader.load(mod).info.web:
		return auth_(render_template('module.html', mod=mod))
	else:abort(404)

@web.route("/get")
def preloading():

	if request.args.get('data').startswith('module'):
		return auth_(loader.load(request.args.get('data').replace('module/','')).web_panel(web))

	if request.args.get('data')=='home_preloader':
		if not utils.me: utils.me=app.get_me()
		photo=[t for t in app.get_chat_photos("me")]
		if photo:
			tmp=db.select('info', 'logo')[list(db.select('info', 'logo'))[-1]].logo if db.select('info', 'logo') else None
			if photo[-1].file_unique_id!=tmp:
				app.download_media(app.get_chat_photos("me", limit=1)[0].file_id, file_name="static/img/ava.png")
				db.insert('info', 'logo', f'"{photo[-1].file_unique_id}"')
			ava=True
		else: ava=False
		data=Box({
			'cpu': int(psutil.cpu_percent(4)),
			'disk': int(psutil.disk_usage('/').percent),
			'user': utils.me,
			'avatar': 'ava' if ava else 'logo',
			'release': utils.config.version
		})
		out=''
		tmp2=open('templates/list_mod.html', 'r').read()
		i=0
		for mod in loader.list():
			web_panel_=f'<div onclick="loading(\'/modules/{mod}\');" class="badge bgc-info"><i class="bi bi-globe"></i> Web</div>' if loader.load(mod).info.web else ''
			out+=tmp2.format(mod=loader.load(mod).info, raw_name=mod, index=i, web_panel_=web_panel_)
			i+=1
		tmp=open('templates/home_load.html', 'r').read()
		return auth_(tmp.format(data=data, modules=out))
		

@web.after_request
def add_header(r):
	
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r 

if os.path.isfile('settings.json'):
	try:os.remove('databases/logs.db')
	except:pass
	import asyncio, time, traceback, psutil
	from pyrogram import Client
	from core.utils import utils, DataBase, Logs
	from core.loader import loader
	from threading import Timer

	db=DataBase()
	logs=Logs()
	
	if not os.path.exists('databases/main.db'):
		db.create('info', (
				db.Column('logo'),
			))

	if __name__=='__main__':
		print(tabulate([["liri0t", "Addres web panel", "Modules"], [f"v-{utils.config.version}", "127.0.0.1:5000", len(loader.list())]], tablefmt="grid"))
		Thread(target=serve, args=(web,), kwargs={'host': '0.0.0.0', 'port': 5000, 'threads': 10}, daemon=True).start()
		app=Client('liri0t', api_id=utils.config.api_id, api_hash=utils.config.api_hash, plugins={'root': 'plugins/'})
		logs.add('info', 'Started')
		app.run()
		
else:
	print(tabulate([["liri0t", "Addres web panel"], [f"Creating app", "127.0.0.1:5000"]], tablefmt="grid"))
	serve(web, host='0.0.0.0', threads=10, port=5000)
