# -*- coding: utf-8 -*-
""" A lightweight wrapper for the Funkwhale API."""
import requests

class APIError(Exception):
	pass

class Session(object):

	def __init__(self, instance_endpoint="https://demo.funkwhale.audio", username="demo", password="demo", token=None, api_prefix="/api/", api_version="v1/"):
		""" Funkwhale python API wrapper:
		:param instance_endpoint (optional): URL of the funkwhale instance to connect. If no value is specified, it will connect to the default demo instance.
		:param username (optional): Username to use during authentication, if token is not provided.
		:param password (optional): password for the username when authenticating. If token is provided then username and password are not needed.
		:param token (optional): JWT token to be used for authentication. Normally this token is given by /api/v1/token and it replaces user and password in Funkwhale.
		:param api_prefix (optional): API prefix to be used during calls to method. This shouldn't be changed unless funkwhale implements its API in a path different than /api.
		:param api_version (optional): API version to use. This shouldn't be changed for now as there is only an API version (v1), but it may be useful for future API versions.
		"""

		self.http = requests.Session()
		self.username = username
		self.password = password
		self.instance_endpoint = instance_endpoint
		self.token = token
		self.API_PREFIX = api_prefix
		if self.API_PREFIX.endswith("/") == False:
			self.API_PREFIX = self.API_PREFIX + "/"
		self.API_VERSION = api_version
		if self.API_VERSION.endswith("/") == False:
			self.API_VERSION = self.API_VERSION + "/"

	def login(self):
		""" Attempts to login if a password and username have been supplied and no access token is defined, yet. """
		if self.token is not None:
			self.http.headers.update(Authorization="Bearer "+self.token)
		else:
			if self.username is None or self.password is None:
				raise ValueError("If token is not provided, you need both user and password for getting a token")
			result = self.post("token/", username=self.username, password=self.password)
			self.token = result["token"]
			self.http.headers.update(Authorization="Bearer "+self.token)

	def post(self, method, **params):
		""" Helper for all post methods. This should not be used directly. """
		response = self.http.post(self.instance_endpoint+self.API_PREFIX+self.API_VERSION+method, data=params)
		if response.ok == False:
			raise APIError("Error {error_code}: {text}".format(error_code=response.status_code, text=response.text))
		return response.json()

	def get(self, method, **params):
		""" Helper for all GET methods. This should not be used directly. """
		response = self.http.get(self.instance_endpoint+self.API_PREFIX+self.API_VERSION+method, params=params)
		if response.ok == False:
			raise APIError("Error {error_code}: {text}".format(error_code=response.status_code, text=response.text))
		return response.json()

	def method(self, method, *args, **kwargs):
		""" Receives method and arguments and calls the appropiate function. This shouldn't be called directly. """
		# determines kind of method
		extension = method.split(".")[-1]
		method = method.replace("."+extension, "")
		method = method.replace(".", "/")
		if len(args) == 1:
			if method.endswith("/libraries"):
				method = method.replace("/libraries", "/{id}/libraries".format(id=args[0]))
			else:
				method = method+"/{id}".format(id=args[0])
		result = getattr(self, extension)(method=method, **kwargs)
		return result

	def get_api(self):
		""" Retrieves the "real" API from where you can start calling everything right after logging into Funkwhale. """
		return API(self)

class API(object):
	__slots__ = ('_session', '_method')

	def __init__(self, session, method=None):
		self._session = session
		self._method = method

	def __getattr__(self, method):
		if '_' in method:
			m = method.split('_')
			method = m[0] + ''.join(i.title() for i in m[1:])
		return API(self._session, (self._method + '.' if self._method else '') + method)

	def __call__(self, *args, **kwargs):
		return self._session.method(self._method, *args, **kwargs)

	def full_url(self, method):
		""" Converts a partial URL such as /api/v1/listen/{id} into https://instance.endpoint/api/v1/listen/track_id """
		# check if the method is valid.
		if method.startswith(self._session.API_PREFIX) == False:
			raise ValueError("the method passed seems to be an invalid URL.")
		return self._session.instance_endpoint+method