aioec
=====

An aiohttp-based client for the `Emoji Connoisseur API <https://emoji-connoisseur.python-for.life>`_.


Usage
----

.. code-block:: python

	import aioec

	client = aioec.Client(token='your token here')
	# if no token is provided, only anonymous endpoints will be available

	# this step isn't necessary but makes sure that your token is correct
	await client.login()

	# in a coroutine...
	emote = await client.emote('Think')
	emote.name  # Think

	await emote.edit(name='Think_', description='a real happy thinker')
	# remove the description:
	await emote.edit(description=None)

	for gamewisp_emote in await client.search('GW'):
		await gamewisp_emote.delete()

	all_emotes = await client.emotes()
	popular_emotes = await client.popular()

	await client.close()

	# it's also a context manager:
	async with aioec.Client(token=my_token) as client:
		await client.delete('Think_')
	# this will automatically close the client

License
-------

MIT/X11

Copyright © 2018 Benjamin Mintz <bmintz@protonmail.com>
