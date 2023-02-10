import unittest

from ci_server import app

class TestUpdater(unittest.TestCase):
	def setUp(self):
		app.testing = True
		self.app = app.test_client()

	def tearDown(self):
		pass

	# Only a user agent that starts with 'GitHub-Hookshot' should be allowed
	def test_disallow_ua_not_github(self):
		response = self.app.post("/", headers={'User-Agent': 'Firefox'})
		self.assertEqual(response.status_code, 403)

	# A ping event should return a 200 status code and an empty JSON object
	def test_ping(self):
		response = self.app.post("/", headers={'User-Agent': 'GitHub-Hookshot', 'X-GitHub-Event': 'ping'})
		self.assertEqual(response.status_code, 200)

	# A push event should return a 200 status code
	def test_push(self):
		response = self.app.post("/", headers={'User-Agent': 'GitHub-Hookshot', 'X-GitHub-Event': 'push'})
		self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
	unittest.main()
