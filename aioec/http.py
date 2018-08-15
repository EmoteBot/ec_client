import asyncio
import json
import sys
from urllib.parse import quote as _uriquote

import aiohttp

from .errors import HttpException, Forbidden, LoginFailure, NotFound
from .utils import sentinel
from . import __version__

# Using code provided by Rapptz
# Copyright © 2015–2017 Rapptz
# https://github.com/Rapptz/discord.py/blob/4aecdea0524e7b481f9750166bf9e9be287ec445/discord/http.py

async def json_or_text(response):
	text = await response.text(encoding='utf-8')
	if response.content_type == 'application/json':
		return json.loads(text)
	return text

class Route:
	BASE = 'http://emoji-connoisseur.python-for.life/api/v0'

	def __init__(self, method, path, **parameters):
		self.path = path
		self.method = method
		url = (self.BASE + self.path)
		if parameters:
			self.url = url.format(**{k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
		else:
			self.url = url

class HttpClient:
	def __init__(self, token=None, *, loop=None):
		self.token = token
		self.loop = loop or asyncio.get_event_loop()
		user_agent = 'aioec (https://github.com/bmintz/aioec {0} aiohttp/{2} Python/{1[0]}.{1[1]} aiohttp/{2}'
		self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

		headers = {'User-Agent': self.user_agent}
		if self.token is not None:
			headers['Authorization'] = self.token

		self._session = aiohttp.ClientSession(headers=headers, loop=self.loop)

	async def request(self, route, **kwargs):
		method = route.method
		url = route.url

		async with self._session.request(method, url, **kwargs) as response:
			data = await json_or_text(response)
			if response.status in range(200, 300):
				return data

			if response.status == 401:
				raise LoginFailure
			elif response.status == 403:
				raise Forbidden(response, data)
			elif response.status == 404:
				raise NotFound(response, data)
			else:
				raise HTTPException(response, data)

	def emotes(self):
		return self.request(Route('GET', '/emotes'))

	def emote(self, name):
		return self.request(Route('GET', '/emote/{name}', name=name))

	def create(self, name, url):
		return self.request(Route('PATCH', '/emote/{name}/{url}', name=name, url=url))

	def edit(self, name_, *, name=None, description=sentinel):
		data = {}

		# we perform this dance so that the caller can run it like edit_emote('foo', name='bar')
		new_name = name
		name = name_

		if new_name is not None:
			data['name'] = new_name
		if description is not sentinel:  # None is an allowed value for description
			data['description'] = description

		return self.request(Route('PATCH', '/emote/{name}', name=name), json=data)

	def delete(self, name):
		return self.request(Route('DELETE', '/emote/{name}', name=name))

	def search(self, query):
		return self.request(Route('GET', '/search/{query}', query=query))

	def popular(self):
		return self.request(Route('GET', '/popular'))
