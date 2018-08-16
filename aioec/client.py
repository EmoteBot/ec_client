from .http import HttpClient
from .emote import Emote
from . import utils

class Client:
	def __init__(self, token=None, *, loop=None):
		self._http = HttpClient(token=token, loop=loop)

	def _new_emote(self, data):
		return Emote(data=data, http=self._http)

	def close(self):
		return self._http.close()

	async def emotes(self):
		return map(self._new_emote, await self._http.emotes())

	async def search(self, query):
		return map(self._new_emote, await self._http.search(query))

	async def popular(self):
		return map(self._new_emote, await self._http.popular())

	async def emote(self, name):
		return self._new_emote(await self._http.emote(name))

	async def login(self):
		"""Checks that your token is correct.

		Returns the user ID associated with your token.
		"""

		return int(await self._http.login())

	async def create(self, name, url):
		return self._new_emote(await self._http.create(name, url))

	async def edit(self, name_, *, name=None, description=utils.sentinel):
		return self._new_emote(await self._http.edit(name_, name=name, description=description))

	async def delete(self, name):
		return self._new_emote(await self._http.delete(name))

	async def __aenter__(self):
		return self

	def __aexit__(self, *_):
		return self.close()
