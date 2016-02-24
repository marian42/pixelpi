from input import *
from flask import Flask
import thread
import logging

app = Flask(__name__, static_folder='../')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route("/")
def index():
	return app.send_static_file('input/keys.html')

@app.route("/key/<id>")
def key(id):
	press(int(id))
	release(int(id))
	return "ok"

thread.start_new_thread(app.run, (), {'host': '0.0.0.0', 'port': 80})