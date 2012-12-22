import os
from flask import make_response
import re


def get_fixture(name):
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
        return ex.sub('ghapi.herokuapp.com', json)
    return ''


def response_from_fixture(name):
    """Make a response from a fixture."""
    response = make_response()
    response.data = get_fixture(name)
    response.content_type = 'application/json; charset=utf-8'
    response.mimetype = 'application/json'
    return response
