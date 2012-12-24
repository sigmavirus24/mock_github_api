from mock_github_api.core import app
from mock_github_api.helpers import response_from_fixture, boolean_response


@app.route('/user', methods=['GET', 'PATCH'])
def user():
    return response_from_fixture('user', status_code=404)


@app.route('/user/emails', methods=['GET', 'POST', 'DELETE'])
def emails():
    return response_from_fixture('email', True, 404)


@app.route('/user/followers')
@app.route('/user/following')
def iter_following():
    return response_from_fixture('user', True, 404)


@app.route('/user/issues')
def issues():
    return response_from_fixture('issue', True, 404)


@app.route('/user/keys/<id>')
def key(id):
    return response_from_fixture('key', status_code=404)


@app.route('/user/keys')
def keys():
    return response_from_fixture('key', True, 404)


@app.route('/user/orgs')
def orgs():
    return response_from_fixture('org', True, 404)


@app.route('/user/repos')
@app.route('/user/starred')
@app.route('/user/subscriptions')
def repos():
    return response_from_fixture('repo', True, 404)


@app.route('/user/starred/<login>/<repo>', methods=['DELETE', 'PUT'])
@app.route('/user/subscriptions/<login>/<repo>', methods=['DELETE', 'PUT'])
def star_subscribe(login, repo):
    return boolean_response(204)


@app.route('/user/following/<login>', methods=['DELETE'])
def unfollow(login):
    return boolean_response(204)
