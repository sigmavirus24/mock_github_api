from mock_github_api.core import app
from mock_github_api.helpers import (response_from_fixture, boolean_response,
                                     is_authorized, not_authorized_response)


@app.route('/user', methods=['GET', 'PATCH'])
def user():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('user', status_code=404)


@app.route('/user/emails', methods=['GET', 'POST', 'DELETE'])
def emails():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('email', True, 404)


@app.route('/user/followers')
@app.route('/user/following')
def iter_following():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('user', True, 404)


@app.route('/user/issues')
def issues():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('issue', True, 404)


@app.route('/user/keys/<id>')
def key(id):
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('key', status_code=404)


@app.route('/user/keys')
def keys():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('key', True, 404)


@app.route('/user/orgs')
def orgs():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('org', True, 404)


@app.route('/user/repos')
@app.route('/user/starred')
@app.route('/user/subscriptions')
def repos():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('repo', True, 404)


@app.route('/user/starred/<login>/<repo>', methods=['DELETE', 'PUT'])
@app.route('/user/subscriptions/<login>/<repo>', methods=['DELETE', 'PUT'])
def star_subscribe(login, repo):
    if not is_authorized():
        return not_authorized_response()
    return boolean_response(204)


@app.route('/user/following/<login>', methods=['DELETE'])
def unfollow(login):
    if not is_authorized():
        return not_authorized_response()
    return boolean_response(204)
