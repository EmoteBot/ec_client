import asyncio
import json
import sys
from urllib.parse import quote as _uriquote

import aiohttp

from . import __version__

# Using code provided by Rapptz
# Copyright © 2015–2017 Rapptz
# https://github.com/Rapptz/discord.py/blob/4aecdea0524e7b481f9750166bf9e9be287ec445/discord/http.py

async def json_or_text(response):
	text = await response.text(encoding='utf-8')
	if response.headers['content-type'] == 'application/json':
		return json.loads(text)
	return text

class Route:
	BASE = 'https://emoji-connoisseur.python-for.life/api/v0'

	def __init__(self, method, path, **parameters):
		self.path = path
		self.method = method
		url = (self.BASE + self.path)
		if parameters:
			self.url = url.format(**{k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
		else:
			self.url = url

class Client:
	def __init__(self, token=None, *, loop=None):
		self.token = token
		self.loop = loop or asyncio.get_event_loop()
		user_agent = 'aioec (https://github.com/bmintz/aioec {0} aiohttp/{2} Python/{1[0]}.{1[1]} aiohttp/{2}'
		self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)
		self._session = aiohttp.ClientSession(headers={'User-Agent': self.user_agent}, loop=self.loop)

	async def request(self, route, **kwargs):
		method = route.method
		url = route.url

		async with self._session.request(method, url, **kwargs) as response:
			data = await json_or_text(response)
			if response.status in range(200, 300):
				return data

			if response.status == 403:
				raise Forbidden(response, data)
			elif response.status == 404:
				raise NotFound(response, data)
			else:
				raise HTTPException(response, data)

	def emotes(self):
		return self.request(Route('GET', '/emotes'))
