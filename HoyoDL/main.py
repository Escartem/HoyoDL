import requests

class HoyoDL:
	def __init__(self, game=None, version=None, provider=None):
		self.game = game
		self.version = version
		self.provider = provider

		self.config = {
			"defaultProvider": "https://ena.escartem.moe/hoyodl/data.json"
		}

		self.errors = {
			"invalidGame": "Invalid game !",
			"invalidVersion": "Invalid version !",
			"noGame": "Please provide a game before the version !",
			"jsonError": "Error getting data: {0}"
		}

		self.data = self._jsonFromUrl(self.errors["defaultProvider"])

		if game and not self._isGameValid(self.game):
			raise HoyoDLException(self.errors["invalidGame"])

		if version:
			if not game:
				raise HoyoDLException(self.errors["noGame"])
			elif not self._isVersionValid(self.version):
				raise HoyoDLException(self.errors["invalidVersion"])

	def _jsonFromUrl(self, url: str) -> dict:
		try:
			response = requests.get(url)
			response.raise_for_status()
			return response.json()
		except Exception as e:
			raise HoyoDLException(self.errors["jsonError"].format(e))

		return None

	def _isGameValid(self, game: str) -> bool:
		return game in self.data["games"]

	def _isVersionValid(self, version: str) -> bool:
		return version in self.data["games"][self.game]

	# update config
	def setGame(self, game: str) -> None:
		if not self._isGameValid(game):
			raise HoyoDLException(self.errors["invalidGame"])
		self.game = game

	def setVersion(self, version: str) -> None:
		if not self.game:
			raise HoyoDLException(self.errors["noGame"])
		if not self._isVersionValid(version):
			raise HoyoDLException(self.errors["invalidVersion"])
		self.version = version

	def getHash(self):
		pass

	def getFileURL(self):
		pass

	def getBlocks(self):
		pass

	def downloadFile(self):
		pass

class HoyoDLException(Exception):
	def __init__(self, message):
		super().__init__(message)
