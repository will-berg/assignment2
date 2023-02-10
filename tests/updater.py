import unittest
import requests
import json

from updater import app

class TestUpdater(unittest.TestCase):
	def setUp(self):
		app.testing = True
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

	# Only a user agent that starts with 'GitHub-Hookshot' should be allowed
	def test_disallow_ua_not_github(self):
		response = self.app.post("/", headers={'User-Agent': 'Firefox'})
		self.assertEqual(response.status_code, 403)

	# The updater should return a 400 status code if X-GitHub-Event isn't set
	def test_empty_event(self):
		response = self.app.post("/", headers={'User-Agent': 'GitHub-Hookshot'})
		self.assertEqual(response.status_code, 400)

	# A ping event should return a 200 status code and an empty JSON object
	def test_ping(self):
		response = self.app.post("/", headers={'User-Agent': 'GitHub-Hookshot', 'X-GitHub-Event': 'ping'}, data="{}")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.text.strip(), '{}')

	# An unsupported event should return a 400 status code
	def test_unsupported_event(self):
		response = self.app.post("/", headers={'User-Agent': 'GitHub-Hookshot', 'X-GitHub-Event': 'deadbeef'}, data="{}")
		self.assertEqual(response.status_code, 400)

	# A push event should return a 200 status code
	def test_push_on_main(self):
		data = {
			"ref": "refs/heads/main"
		}
		response = self.app.post("/", headers={'User-Agent': 'GitHub-Hookshot', 'X-GitHub-Event': 'push'}, data=json.dumps(data))
		self.assertEqual(response.status_code, 200)

	# A push event on a branch that isn't main shouldn't run the update
	def test_push_on_bogus(self):
		data = {
			"ref": "refs/heads/bogus"
		}
		response = self.app.post("/", headers={'User-Agent': 'GitHub-Hookshot', 'X-GitHub-Event': 'push'}, data=json.dumps(data))

		# The webhook should still return a 200 status code,
		# since there is nothing wrong with the request,
		# it just won't be acted upon.
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.data)
		self.assertTrue(data["message"].lowercase().find('skip') != -1)

if __name__ == '__main__':
	unittest.main()