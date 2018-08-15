# Using code provided by Rapptz
# Copyright © 2015–2017 Rapptz
# https://github.com/Rapptz/discord.py/blob/f25091efe1281aebe70189c61f9cac405b21a72f/discord/errors.py

class HTTPException(Exception):
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
			self.text = message['message']
		else:
			self.text = message

		fmt = '{0.reason} (status code: {0.status})'
		if self.text:
			fmt = fmt + ': {1}'

		super().__init__(fmt.format(self.response, self.text))

class Forbidden(HTTPException):
	"""Exception that's thrown for when status code 403 occurs.

	Subclass of :exc:`HTTPException`
	"""
	pass

class NotFound(HTTPException):
	"""Exception that's thrown for when status code 404 occurs.

	Subclass of :exc:`HTTPException`
	"""
	pass
