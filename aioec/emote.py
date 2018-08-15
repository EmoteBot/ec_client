from . import utils

class Emote:
	__slots__ = frozenset((
		'_data',
		'_http',
		'_name',
		'_id',
		'_author',
		'_animated',
		'_created',
		'_modified',
		'_preserve',
		'_description',
		'_usage',
	))

	def __new__(cls, *, data, http):
		self = super().__new__(cls)

		self._http = http
		self._data = data

		for key, value in data.items():
			if key in {'created', 'modified'} and value:
				value = utils.epoch_time(value)
			setattr(self, '_' + key, value)

		return self


	for field in __slots__:
		def getter(self, field=field):
			return getattr(self, field)

		public_name = field[1:]
		getter.__name__ = public_name
		vars()[public_name] = property(getter)
		del getter, public_name

	del field

	def _new_emote(self, data):
		return type(self)(http=self._http, data=data)

	async def delete(self):
		return self._new_emote(await self._http.delete(self.name))

	async def edit(self, *, name=None, description=utils.sentinel):
		return self._new_emote(await self._http.edit(self.name, name=name, description=description))

	@property
	def usage(self):
		return getattr(self, '_usage', None)

	@property
	def url(self):
		return 'https://cdn.discordapp.com/emojis/{0.id}.{ext}?v=1'.format(
			self,
			ext='gif' if self.animated else 'png')

	@property
	def _a(self):
		return 'a' if self.animated else ''

	@property
	def as_reaction(self):
		return '{self._a}:{0.name}:{0.id}'.format(self)

	def __str__(self):
		return '<{self._a}:{0.name}:{0.id}>'.format(self)

	def __repr__(self):
		return (
			'{0.__module__}.{0.__class__.__qualname__}'
			'<name={0.name}, id={0.id}, animated={0.animated}>'.format(self))
