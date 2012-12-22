from flask import Flask, render_template
from mock_github_api.helpers import response_from_fixture

app = Flask(__name__)

ROBOTS = """User-agent: *"""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def auth_user():
    response = response_from_fixture('user')
    if response.data is '':
        response.status_code = 404
    return response


@app.route('/users/<login>')
def get_user(login):
    response = response_from_fixture('user')
    if response.data is '':
        response.status_code = 404
    return response
