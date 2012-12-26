import mock_github_api.core
import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        mock_github_api.core.app.config['TESTING'] = True
        self.app = mock_github_api.core.app.test_client()

    def test_index(self):
        index = self.app.get('/')
        assert index.data.startswith('<!DOCTYPE html>')

    def test_robots(self):
        robots = self.app.get('/robots.txt')
        assert 'User-agent' in robots.data

    def test_user(self):
        user = self.app.get('/user')
        assert user.status_code == 401
        user = self.app.patch('/user')
        assert user.status_code == 401
        user = self.app.get('/user', headers={
            'Authorization': 'Basic Zm9vOmJhcg=='})
        assert user.status_code == 200
        user = self.app.patch('/user', headers={
            'Authorization': 'Basic Zm9vOmJhcg=='})
        assert user.status_code == 200


if __name__ == '__main__':
    unittest.main()
