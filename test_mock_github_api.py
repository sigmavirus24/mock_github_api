import mock_github_api.core
import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        mock_github_api.core.app.config['TESTING'] = True
        self.app = mock_github_api.core.app.test_client()
        self.auth_headers = {'Authorization': 'Basic Zm9vOmJhcg=='}
        self.json_headers = {'Content-Type': 'application/json'}
        self.headers = self.auth_headers.copy()
        self.headers.update(self.json_headers)

    def assert_all(self, iterable, status_code):
        assert all([i.status_code == status_code for i in iterable])

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

    def test_user_emails(self):
        path = '/user/emails'
        calls = (self.app.get, self.app.post, self.app.delete)
        # Un-authorized
        emails = self.make_calls(path, calls)
        self.assert_all(emails, 401)
        # Authorized
        email = self.app.get(path, headers=self.headers)
        assert email.status_code == 200
        email = self.app.post(path, data='["foo@bar.com"]',
                              headers=self.headers)
        assert email.status_code == 201

        email = self.app.delete(path, data='["foo@bar.com"]',
                                headers=self.headers)
        assert email.status_code == 204


if __name__ == '__main__':
    unittest.main()
