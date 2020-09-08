import logging
from flask import Flask
from flask import jsonify
from flask import request

from targets.email import TargetEmail
from targets.http import TargetHttp

app = Flask(__name__)

# TODO: create yaml config
TARGETS = [
	TargetHttp('http://localhost/'),
	TargetEmail(
		domain='smtp.yandex.ru',
		login='cdc3511a26f029453020572b2@yandex.ru',
		password='cdc3511a26f029453020572b2c26c263',
		recipients=['vladimirfol@gmail.com'],
	),
]

@app.route('/')
def index():
	for target in TARGETS:
		try:
			target.handle(request)
		except Exception as exc:
			logging.exception(f'unhandled exception on target {target} : {exc}')
	return jsonify({'text': 'ok'})
