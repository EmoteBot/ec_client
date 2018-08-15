from .http import HttpClient
from .emote import Emote
from . import utils

class Client:
	def __init__(self, token=None, *, loop=None):
		self._http = HttpClient(token=token, loop=loop)

	def _new_emote(self, data):
		return Emote(data=data, http=self._http)

	async def emotes(self):
		return map(self._new_emote, await self._http.emotes())

	async def search(self, query):
		return map(self._new_emote, await self._http.search(query))

	async def popular(self):
		return map(self._new_emote, await self._http.popular())

	async def emote(self, name):
		return self._new_emote(await self._http.emote(name))

	async def create(self, name, url):
		return self._new_emote(await self._http.create(name, url))

	async def edit(self, name_, *, name=None, description=utils.sentinel):
		return self._new_emote(await self._http.edit(name_, name=name, description=description))

	async def delete(self, name):
		return self._new_emote(await self._http.delete(name))
