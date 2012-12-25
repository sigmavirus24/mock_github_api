import os
from flask import make_response, request
import re
from datetime import datetime


def get_fixture(name, array=False):
    if hasattr(get_fixture, '_re'):
        ex = get_fixture._re
    else:
        ex = re.compile('api\.github\.com')
        setattr(get_fixture, '_re', ex)

    directory = os.path.dirname(__file__)
    fixture = os.path.join(directory, 'fixtures', name)
    print fixture
    if os.path.isfile(fixture):
        json = open(fixture).read()
        if array:
            json = '[{0}]'.format(json)
        return ex.sub('ghapi.herokuapp.com', json)
    return ''


def _json_response(paginate):
    response = make_response()
    response.content_type = 'application/json; charset=utf-8'
    response.mimetype = 'application/json'
    response.headers.add('x-ratelimit-remaining', '5000')
    response.headers.add('x-ratelimit-limit', '5000')
    response.headers.add('date', datetime.now().strftime(
        '%a, %d %b %Y %H:%M%S GMT'))
    response.headers.add('x-github-media-type', parse_accept())
    if paginate:
        root = request.url_root
        end = request.endpoint
        response.headers.add('Link', '<{0}{1}?page=2&per_page=1>; '
                             'rel="next", <{0}{1}?page=100&per_page=1>; '
                             'rel="last"'.format(root, end))
    return response


def response_from_fixture(name, array=False, status_code=404, paginate=False):
    """Make a response from a fixture."""
    response = _json_response(paginate)
    response.data = get_fixture(name, array)
    if response.data is '':
        response.status_code = status_code
    return response


def boolean_response(status_code):
    """Make a response with no data, only a status code."""
    response = _json_response()
    response.status_code = status_code
    return response


def not_authorized_response():
    """Respond that the user is not authorized."""
    response = _json_response()
    response.status_code = 401
    response.data = '{"message": "Requires authentication"}'
    return response


def is_authorized():
    """Checks to see if a request has an authorization header or a
    client_id/client_secret pair in the query string."""
    args = request.args
    header = request.authorization is not None
    params = args.get('client_id', None) and args.get('client_secret', None)
    return header or params


def parse_accept():
    """Parse the Accept Header like GitHub does."""
    if hasattr(parse_accept, '_re'):
        ex = parse_accept._re
    else:
        ex = re.compile('\w+/vnd\.(?P<github>github\.\w+)\.?'
                        '(?P<param>\w+)?\+(?P<format>\w+)')
        parse_accept._re = ex

    header = request.headers.get('Accept')
    match = ex.match(header)

    if not (match and header):
        return ''

    if match.group('param'):
        return '{0}; param={1}; format={2}'.format(match.group('github'),
                                                   match.group('param'),
                                                   match.group('format'))

    return '{0}: format={1}'.format(match.group('github'),
                                    match.group('format'))
