import mock_github_api.core
import unittest
import json


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        mock_github_api.core.app.config['TESTING'] = True
        self.app = mock_github_api.core.app.test_client()
        self.headers = {
            'Authorization': 'Basic Zm9vOmJhcg==',
        }
        self.conf = {
            'content_type': 'application/json',
            'headers': self.headers,
        }

    def assert_all(self, iterable, status_code):
        assert all([i.status_code == status_code for i in iterable])

    def status_code(self, response, code):
        assert response.status_code == code, (
            'Expected %d but got %d' % (code, response.status_code)
        )

    def make_calls(self, path, calls, **kwargs):
        return [c(path, **kwargs) for c in calls]

    def test_index(self):
        index = self.app.get('/')
        assert index.data.startswith('<!DOCTYPE html>')

    def test_robots(self):
        robots = self.app.get('/robots.txt')
        assert 'User-agent' in robots.data

    def test_user(self):
        path = '/user'
        calls = (self.app.get, self.app.patch)
        # Un-authorized
        users = self.make_calls(path, calls)
        self.assert_all(users, 401)
        # Authorized
        users = self.make_calls(path, calls, headers=self.headers)
        self.assert_all(users, 200)

    def test_unauth_user_emails(self):
        path = '/user/emails'
        calls = (self.app.get, self.app.post, self.app.delete)
        emails = self.make_calls(path, calls)
        self.assert_all(emails, 401)

    def test_get_user_emails(self):
        path = '/user/emails'
        email = self.app.get(path, headers=self.headers)
        self.status_code(email, 200)

    def test_post_user_emails(self):
        path = '/user/emails'
        #print self.headers
        data = json.dumps(['foo@bar.com'])
        email = self.app.post(path, data=data, **self.conf)
        self.status_code(email, 201)

    def test_delete_user_emails(self):
        path = '/user/emails'
        email = self.app.delete(path, data='["foo@bar.com"]', **self.conf)
        self.status_code(email, 204)

    def test_user_followers(self):
        path = '/user/followers'
        rv = self.app.get(path)
        self.status_code(rv, 401)

        rv = self.app.get(path, headers=self.headers)
        self.status_code(rv, 200)

    def test_user_following(self):
        path = '/user/following'
        rv = self.app.get(path)
        self.status_code(rv, 401)

        rv = self.app.get(path, headers=self.headers)
        self.status_code(rv, 200)

    def test_user_is_following(self):
        path = '/user/following/sigmavirus24'
        calls = (self.app.get, self.app.put, self.app.delete)
        emails = self.make_calls(path, calls)
        self.assert_all(emails, 401)

    def test_get_user_is_following(self):
        path = '/user/following/sigmavirus24'
        rv = self.app.get(path, headers=self.headers)
        self.status_code(rv, 204)

    def test_put_user_is_following(self):
        path = '/user/following/sigmavirus24'
        rv = self.app.put(path, headers=self.headers)
        self.status_code(rv, 204)

    def test_delete_user_is_following(self):
        path = '/user/following/sigmavirus24'
        rv = self.app.delete(path, headers=self.headers)
        self.status_code(rv, 204)


if __name__ == '__main__':
    unittest.main()
