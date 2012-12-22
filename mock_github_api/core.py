from flask import Flask, render_template

app = Flask(__name__)

ROBOTS = """User-agent: *"""


@app.route('/')
def index():
    return render_template('index.html')
