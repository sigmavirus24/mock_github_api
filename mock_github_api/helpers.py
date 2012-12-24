import os
from flask import make_response
import re


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


def response_from_fixture(name, array=False, status_code=404):
    """Make a response from a fixture."""
    response = make_response()
    response.data = get_fixture(name, array)
    if response.data is '':
        response.status_code = status_code
    response.content_type = 'application/json; charset=utf-8'
    response.mimetype = 'application/json'
    return response


def boolean_response(status_code):
    """Make a response with no data, only a status code."""
    response = make_response()
    response.content_type = 'application/json; charset=utf-8'
    response.mimetype = 'application/json'
    response.status_code = status_code
    return response
