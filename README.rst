ec_client
=====

A requests-based client for the `Emote Collector API <https://emote-collector.python-for.life/api/v0/docs>`_.


Usage
-----

.. code-block:: python3

	import ec_client

	client = ec_client.Client('your token here')
	# if no token is provided, only anonymous endpoints will be available

	# this step isn't necessary but makes sure that your token is correct
	my_user_id = client.login()
	# it returns the user ID associated with your token

	emote = client.emote('Think')
	emote.name  # Think

	emote.edit(name='Think_', description='a real happy thinker')
	# remove the description:
	emote.edit(description=None)

	for gamewisp_emote in client.search('GW'):
		gamewisp_emote.delete()

	all_emotes = client.emotes()
	popular_emotes = client.popular()

	client.close()

	# it's also a context manager:
	with aioec.Client(token=my_token) as client:
		client.delete('Think_')
	# this will automatically close the client

License
-------

MIT/X11

Copyright © 2018 Benjamin Mintz <bmintz@protonmail.com>
