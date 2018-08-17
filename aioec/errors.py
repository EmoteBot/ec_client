# Using code provided by Rapptz
# Copyright © 2015–2017 Rapptz
# https://github.com/Rapptz/discord.py/blob/f25091efe1281aebe70189c61f9cac405b21a72f/discord/errors.py

class AioEcError(Exception):
	"""
	Base exception type for the library.
	Can be used to catch any exception raised by this library.
	"""
	pass

class ClientException(AioEcError):
	"""Exception that's thrown when an operation in the :class:`Client` fails.

	These are usually for exceptions that happened due to user input.
	"""
	pass

class LoginFailure(ClientException):
	"""Improper or incorrect token has been passed"""
	def __init__(self):
		super().__init__('Invalid or incorrect token has been passed.')

class HttpException(AioEcError):
	"""Exception that's thrown when an HTTP request operation fails.

	Attributes
	------------
	response: aiohttp.ClientResponse
		The response of the failed HTTP request. This is an
		instance of `aiohttp.ClientResponse`__. In some cases
		this could also be a ``requests.Response``.

		__ http://aiohttp.readthedocs.org/en/stable/client_reference.html#aiohttp.ClientResponse

	text: :class:`str`
		The text of the error. Could be an empty string.
	status: :class:`int`
		The status code of the HTTP request.
	code: :class:`int`
		The Discord specific error code for the failure.
	"""

	def __init__(self, response, message):
		self.response = response
		self.status = response.status
		if isinstance(message, dict):
			self.text = message.get('message')
		else:
			self.text = message

		fmt = '{0.reason} (status code: {0.status})'
		if self.text:
			fmt = fmt + ': {1}'

		super().__init__(fmt.format(self.response, self.text))

class Forbidden(HttpException):
	"""Exception that's thrown for when status code 403 occurs.

	Subclass of :exc:`HttpException`
	"""
	pass

class NotFound(HttpException):
	"""Exception that's thrown for when status code 404 occurs.

	Subclass of :exc:`HttpException`
	"""
	pass

class EmoteExists(HttpException):
	"""Exception that's thrown for when status code 404 occurs.
	This happens when an emote already exists with the given name and you tried to create a new one
	with that name.

	Subclass of :exc:`HttpException`
	"""
	def __init__(self, response, name):
		self.name = name
		super().__init__(response, 'An emote called {} already exists'.format(name))
