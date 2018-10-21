from .http import HttpClient
from .emote import Emote
from . import utils

class Client:
	def __init__(self, token=None):
		self._http = HttpClient(token=token)

	def _new_emote(self, data):
		return Emote(data=data, http=self._http)

	def close(self):
		return self._http.close()

	def emote(self, name):
		return self._new_emote(self._http.emote(name))

	def emotes(self):
		return list(map(self._new_emote, self._http.emotes()))

	def search(self, query):
		return list(map(self._new_emote, self._http.search(query)))

	def popular(self):
		return list(map(self._new_emote, self._http.popular()))

	def login(self):
		"""Checks that your token is correct.

		Returns the user ID associated with your token.
		"""

		return int(self._http.login())

	def create(self, *, name, url=None, image=None):
		"""Create an emote. Exactly one of url or image is required.

		Raises:
			:class:`RequestEntityTooLarge`: the emote exceeded 16 MiB, or took too long to resize.
			:class:`UnsupportedMediaType`: the emote was not a PNG, GIF, or JPEG.
		"""
		return self._new_emote(self._http.create(name=name, url=url, image=image))

	def edit(self, name_, *, name=None, description=utils.sentinel):
		return self._new_emote(self._http.edit(name_, name=name, description=description))

	def delete(self, name):
		return self._new_emote(self._http.delete(name))

	def __enter__(self):
		return self

	def __exit__(self, *_):
		return self.close()
