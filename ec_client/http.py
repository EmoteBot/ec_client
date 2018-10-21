import functools
import json
import sys
from urllib.parse import quote

import requests

from .errors import (
	EmoteDescriptionTooLongError,

	HttpException,
	Forbidden,
	LoginFailure,
	NotFound,
	EmoteExists,
	RequestEntityTooLarge,
	UnsupportedMediaType)
from .utils import sentinel
from . import __version__

# Using code provided by Rapptz
# Copyright © 2015–2017 Rapptz
# https://github.com/Rapptz/discord.py/blob/4aecdea0524e7b481f9750166bf9e9be287ec445/discord/http.py

# by default, quote doesn't quote /, which we don't want.
# quote_plus does, but it also encodes " " as "+", which we don't want.
uriquote = functools.partial(quote, safe='')
del quote

def json_or_text(response):
	try:
		return response.json()
	except json.JSONDecodeError:
		return response.text

class Route:
	BASE = 'https://emote-collector.python-for.life/api/v0'

	def __init__(self, method, path, **parameters):
		self.path = path
		self.method = method
		url = (self.BASE + self.path)
		if parameters:
			self.url = url.format(**{k: uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
		else:
			self.url = url

class HttpClient:
	def __init__(self, token=None):
		self.token = token
		user_agent = 'ec_client (https://github.com/EmoteCollector/ec_client) {0} requests/{1} Python/{2[0]}.{2[1]}'
		self.user_agent = user_agent.format(__version__, requests.__version__, sys.version_info)
		self._session = requests.Session()

		headers = {'User-Agent': self.user_agent}
		if self.token is not None:
			headers['Authorization'] = self.token

		self._session.headers.update(headers)

	def close(self):
		return self._session.close()

	def request(self, route, **kwargs):
		method = route.method
		url = route.url

		with self._session.request(method, url, **kwargs) as response:
			data = json_or_text(response)
			if response.status_code in range(200, 300):
				return data

			if response.status_code == 401:
				raise LoginFailure
			elif response.status_code == 403:
				raise Forbidden(response, data)
			elif response.status_code == 404:
				raise NotFound(response, data)
			elif response.status_code == 409:  # Conflict
				raise EmoteExists(response, data['name'])
			elif response.status_code == 413:
				raise RequestEntityTooLarge(response, data.get('max_size'), data.get('actual_size'))
			elif response.status_code == 415:
				raise UnsupportedMediaType
			else:
				raise HttpException(response, data)

	def _get_or_empty_list(func):
		def wrapped(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except NotFound:
				return []
		return wrapped

	@_get_or_empty_list
	def emotes(self):
		return self.request(Route('GET', '/emotes'))

	def emote(self, name):
		return self.request(Route('GET', '/emote/{name}', name=name))

	def login(self):
		return self.request(Route('GET', '/login'))

	def create(self, *, name, url=None, image: bytes = None):
		if not url and not image or url and image:
			raise InvalidArgument('exactly one of url or image is required')

		if url:
			return self.request(Route('PUT', '/emote/{name}/{url}', name=name, url=url))

		if image:
			return self.request(Route('PUT', '/emote/{name}', name=name), data=image)

	def edit(self, name_, *, name=None, description=sentinel):
		data = {}

		# we perform this dance so that the caller can run it like edit_emote('foo', name='bar')
		new_name = name
		name = name_

		if new_name is not None:
			data['name'] = new_name
		if description is not sentinel:  # None is an allowed value for description
			data['description'] = description

		try:
			return self.request(Route('PATCH', '/emote/{name}', name=name), json=data)
		except RequestEntityTooLarge as exception:
			raise EmoteDescriptionTooLongError(
				max_length=exception.max_size,
				actual_length=exception.actual_size) from None

	def delete(self, name):
		return self.request(Route('DELETE', '/emote/{name}', name=name))

	@_get_or_empty_list
	def search(self, query):
		return self.request(Route('GET', '/search/{query}', query=query))

	@_get_or_empty_list
	def popular(self):
		return self.request(Route('GET', '/popular'))

	del _get_or_empty_list
