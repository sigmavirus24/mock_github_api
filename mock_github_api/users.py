from mock_github_api.core import app
from mock_github_api.helpers import response_from_fixture


@app.route('/users/<login>')
def get_user(login):
    fixture = 'user'
    if login == 'alejandrogomez':
        fixture = 'utf8_user'
    return response_from_fixture(fixture, status_code=404)
