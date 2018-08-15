aioec
=====

An aiohttp-based client for the `Emoji Connoisseur API <https://emoji-connoisseur.python-for.life>`_.


Usage
----

.. code-block:: python

	import aioec

	ec_client = aioec.Client(token='your token here')
	# if no token is provided, only anonymous endpoints will be available

	# in a coroutine...
	emote = await ec_client.emote('Think')
	emote.name  # Think

	await emote.edit(name='Think_', description='a real happy thinker')
	# remove the description:
	await emote.edit(description=None)

	for gamewisp_emote in await client.search('GW'):
		await gamewisp_emote.delete()

	all_emotes = await client.emotes()
	popular_emotes = await client.popular()

License
-------

MIT/X11

Copyright © 2018 Benjamin Mintz <bmintz@protonmail.com>
