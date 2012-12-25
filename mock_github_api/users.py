from mock_github_api.core import app
from mock_github_api.helpers import response_from_fixture


@app.route('/users')
def users():
    return response_from_fixture('user', True, 404, True)


@app.route('/users/<login>')
def get_user(login):
    fixture = 'user'
    if login == 'alejandrogomez':
        fixture = 'utf8_user'
    return response_from_fixture(fixture, status_code=404)


@app.route('/users/<login>/gists')
def user_gists(login):
    return response_from_fixture('gist', True, 404, True)


@app.route('/users/<login>/orgs')
def user_orgs(login):
    return response_from_fixture('org', True, 404, True)


@app.route('/users/<login>/repos')
def user_repos(login):
    return response_from_fixture('repo', True, 404, True)
