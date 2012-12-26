from flask import request
from mock_github_api.core import app
from mock_github_api.helpers import (response_from_fixture,
                                     failed_validation_response)


@app.route('/repositories')
def all_repos():
    return response_from_fixture('repo', True, paginate=True)


@app.route('/repos/<owner>/<repo>', methods=['GET', 'PATCH'])
def repo():
    if request.method == 'PATCH':
        if not (request.json and request.json.get('name')):
            return failed_validation_response()
    return response_from_fixture('repo')


@app.route('/repos/<owner>/<repo>/contributors')
def contributors():
    return response_from_fixture('user', True)


@app.route('/repos/<owner>/<repo>/languages')
def languages():
    return response_from_fixture('languages')


@app.route('/repos/<owner>/<repo>/teams')
def teams():
    return response_from_fixture('team', True)
