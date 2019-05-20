# -*- coding: utf-8 -*-
import unittest
from funkwhale import api

class testApi(unittest.TestCase):

	def setUp(self):
		# For the moment we use the demo Funkwhale server.
		# Later the API wrapper should have the possibility of using environment variables to fill the class constructor.
		self.session = api.Session()

	def test_auth(self):
		""" Testing user authentication against the Funkwhale server. """
		self.session.login()
		self.assertFalse(self.session.token == None)

	def test_invalid_auth(self):
		""" Testing the exception mechanism present in all API methods. """
		self.setUp()
		self.session.username = "demo1"
		self.assertRaises(api.APIError, self.session.login)
		self.setUp()
		self.session.login()

	def test_call_to_normal_methods(self):
		""" Test that we call some endpoints correctly by using the API facilities. """
		api = self.session.get_api()
		artists_without_params = api.artists.get()
		present_keys = ["next", "previous", "results", "count"]
		for i in present_keys:
			self.assertTrue(i in artists_without_params)
		artists_with_params = api.artists.get(page_size=5, playable=True, ordering="-id")
		for i in present_keys:
			self.assertTrue(i in artists_with_params)
		self.assertTrue(len(artists_with_params["results"]) == 5)
		self.assertTrue(artists_with_params["results"][0]["id"] > artists_with_params["results"][-1]["id"])

	def test_call_to_special_methods(self):
		""" Testing some special methods that are processed differently by the API, such as /artists/id, /artists/id/libraries. """
		api = self.session.get_api()
		# Getting the first artist.
		artist = api.artists.get(1)
		#the only thing we can test about artist is that the ID matches and it's a dict object.
		self.assertTrue(type(artist) == dict)
		self.assertTrue(artist["id"] == 1)
		libraries = api.albums.libraries.get(1)

if __name__ == "__main__":
	unittest.main()