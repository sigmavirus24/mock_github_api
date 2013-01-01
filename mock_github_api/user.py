from flask import request
from mock_github_api.core import app
from mock_github_api.helpers import (response_from_fixture, boolean_response,
                                     is_authorized, not_authorized_response,
                                     failed_validation_response)


@app.route('/user', methods=['GET', 'PATCH'])
def user():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('user', status_code=404)


@app.route('/user/emails', methods=['GET', 'POST', 'DELETE'])
def emails():
    if not is_authorized():
        return not_authorized_response()

    valid = False
    data = request.json
    if data:
        is_str = all([isinstance(e, basestring) for e in data])
        if isinstance(data, list) and is_str:
            valid = True

    response = response_from_fixture('emails', True)
    if valid:
        if request.method == 'POST':
            response.status_code = 201
        elif request.method == 'DELETE':
            response = boolean_response(204)
    elif request.method != 'GET':
        response = failed_validation_response()

    return response


@app.route('/user/followers')
@app.route('/user/following')
def iter_following():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('user', True)


@app.route('/user/following/<login>', methods=['GET', 'DELETE'])
def is_following(login):
    if not is_authorized():
        return not_authorized_response()
    return boolean_response(204)


@app.route('/user/issues')
def issues():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('issue', True)


@app.route('/user/keys/<id>', methods=['GET', 'PATCH', 'DELETE'])
def key(id):
    if not is_authorized():
        return not_authorized_response()

    if request.method == 'DELETE':
        return boolean_response(204)
    elif request.method == 'PATCH':
        valid = valid_key = False
        if request.json:
            valid = request.json.get('title') and request.json.get('key')
            key = request.json.get('key', '')
            valid_key = key.startswith('ssh-rsa ') and len(key) >= 8

        if not (valid_key and valid):
            return failed_validation_response()

    return response_from_fixture('key', status_code=404)


@app.route('/user/keys')
def keys():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('key', True)


@app.route('/user/orgs')
def orgs():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('org', True)


@app.route('/user/repos', methods=['GET', 'POST'])
def repos():
    if not is_authorized():
        return not_authorized_response()

    if request.method == 'POST':
        if not (request.json and request.json.get('name')):
            return failed_validation_response()

    return response_from_fixture('repo', True, paginate=True)


@app.route('/user/starred')
@app.route('/user/subscriptions')
def starred_subscribed():
    if not is_authorized():
        return not_authorized_response()
    return response_from_fixture('repo', True, paginate=True)


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
