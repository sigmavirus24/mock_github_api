from flask import Flask, render_template, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/robots.txt')
def robots():
    response = make_response()
    response.data = "User-agent: *"
    response.content_type = "text/plain"
    return response
