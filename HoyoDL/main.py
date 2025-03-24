import json
import requests
from datetime import datetime

class HoyoDL:
	def __init__(self, game=None, version=None, provider=None):
		self.game = game
		self.version = version
		self.provider = provider

		self.config = {
			"defaultProvider": "https://ena.escartem.moe/hoyodl/data.json"
		}

		self.errors = {
			"invalidGame": "Invalid game ! Available games are {0}",
			"invalidVersion": "Invalid version ! It must be between {0} and {1}",
			"noGame": "Please provide a game before the version !",
			"jsonError": "Error getting data: {0}",
			"invalidUrl": "Invalid url, network error or file may not exist !",
			"indexNotAllowed": "Files index is not available for this game !"
		}

		self.data = self._jsonFromUrl(self.config["defaultProvider"])
		self.filesIndex = []

		if game and not self._isGameValid(self.game):
			raise HoyoDLException(self.errors["invalidGame"].format(", ".join(self.data.keys())))

		if version:
			if not game:
				raise HoyoDLException(self.errors["noGame"])
			elif not self._isVersionValid(self.version):
				raise HoyoDLException(self.errors["invalidVersion"].format(self.data[self.game]["minVersion"], list(self.data[self.game]["hashes"].keys())[-1]))

	def _jsonFromUrl(self, url: str) -> dict:
		try:
			response = requests.get(url)
			response.raise_for_status()
			return response.json()
		except Exception as e:
			raise HoyoDLException(self.errors["jsonError"].format(e))

		return None

	def _isGameValid(self, game: str) -> bool:
		return game in self.data

	def _isVersionValid(self, version: str) -> bool:
		return version in self.data[self.game]["hashes"] and version >= self.data[self.game]["minVersion"]

	def _checkUrl(self, url: str) -> bool:
		try:
			response = requests.head(url, allow_redirects=True, timeout=5)
			return response.status_code == 200
		except requests.RequestException:
			return False

	def _downloadInstance(self, url: str) -> requests.Response | None:
		if not self._checkUrl(url):
			raise HoyoDLException(self.errors["invalidUrl"])
			return
		response = requests.get(url, stream=True)
		response.raise_for_status()
		return response

	def _fetchFilesIndex(self) -> None:
		if not self.data[self.game]["filesIndex"]:
			raise HoyoDLException(self.errors["indexNotAllowed"])
			return

		if self.filesIndex:
			return

		url = self.getFileURL(self.data[self.game]["filesIndexOptions"]["index"])
		dl = self._downloadInstance(url)

		for line in dl.iter_lines(decode_unicode=True):
			if len(line) != 0:
				file = json.loads(line)
				self.filesIndex.append({
					"name": file["remoteName"],
					"md5": file["md5"],
					"size": file["fileSize"]
				})

	# update config
	def setGame(self, game: str) -> None:
		if not self._isGameValid(game):
			raise HoyoDLException(self.errors["invalidGame"].format(", ".join(self.data.keys())))
		self.game = game
		self.filesIndex.clear()

	def setVersion(self, version: str) -> None:
		if not self.game:
			raise HoyoDLException(self.errors["noGame"])
		if not self._isVersionValid(version):
			raise HoyoDLException(self.errors["invalidVersion"].format(self.data[self.game]["minVersion"], list(self.data[self.game]["hashes"].keys())[-1]))
		self.version = version
		self.filesIndex.clear()

	# get elements
	def getHash(self) -> str:
		return self.data[self.game]["hashes"][self.version]

	def getReleaseDate(self, raw: bool=False) -> str:
		_hash = self.getHash()
		timestamp = _hash.split("_")[0]
		if raw:
			return timestamp
		dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
		day = dt.day
		suffix = "th" if 11 <= dt.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(dt.day % 10, "th")
		return f"{dt.strftime('%B')} {day}{suffix}, {dt.year} at {dt.strftime('%H:%M:%S')}"

	def getFileURL(self, path):
		data = self.data[self.game]
		url = f'{data["scatterURL"].replace("$0", data["hashes"][self.version])}/{path}'
		return url

	def getAllBlockFiles(self):
		self._fetchFilesIndex()

		blocks = []
		for file in self.filesIndex:
			if file["name"].startswith(self.data[self.game]["filesIndexOptions"]["blocksRef"]):
				blocks.append(file)

		return blocks

	def downloadBlock(self, id: str, folder: str = "00"):
		data = self.data[self.game]
		ref = f'{data["blocksRef"]}/{folder}/{id}.{data["blocksFormat"]}'
		url = self.getFileURL(ref)
		return self._downloadInstance(url)

	def downloadFile(self, path: str):
		url = self.getFileURL(path)
		return self._downloadInstance(url)

class HoyoDLException(Exception):
	def __init__(self, message):
		super().__init__(message)
