import unittest
import requests

from updater import app

class TestUpdater(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	def tearDown(self):
		pass

	# The updater should not allow GET requests
	def test_get_not_allowed(self):
		response = self.app.get("/")
		self.assertEqual(response.status_code, 405)

	# The updater should allow POST requests
	def test_post_allowed(self):
		response = self.app.post("/")
		self.assertNotEqual(response.status_code, 405)

	# The updater should return a 400 status code if X-GitHub-Event isn't set
	def test_empty_event(self):
		response = self.app.post("/", headers={'User-Agent': 'GitHub-Hookshot'})
		self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
	unittest.main()