import json
import requests
from datetime import datetime

class HoyoDL:
	def __init__(self, game=None, version=None, provider=None):
		self.game = game
		self.version = version
		self.provider = provider

		self.config = {
			"defaultProvider": "https://raw.githubusercontent.com/umaichanuwu/meta/master/hoyodata.json"
		}

		if not self.provider:
			self.provider = self.config["defaultProvider"]

		self.errors = {
			"invalidGame": "Invalid game ! Available games are {0}",
			"invalidVersion": "Invalid version ! It must be between {0} and {1}",
			"noGame": "Please provide a game first !",
			"jsonError": "Error getting data: {0}",
			"invalidUrl": "Failed to fetch, network error or file may not exist !",
			"indexNotAllowed": "Files index is not available for this game !",
			"incompleteSetup": "Missing game and / or version !"
		}

		self.data = self._jsonFromUrl(self.provider)
		self.filesIndex = []

		if game and not self._isGameValid(self.game):
			raise HoyoDLException(self.errors["invalidGame"].format(", ".join(self.data.keys())))

		if version:
			if not game:
				raise HoyoDLException(self.errors["noGame"])
			elif not self._isVersionValid(self.version):
				raise HoyoDLException(self.errors["invalidVersion"].format(self.data[self.game]["minVersion"], list(self.data[self.game]["hashes"].keys())[-1]))

	##########################
	### Internal functions ###
	##########################

	def _jsonFromUrl(self, url: str) -> dict:
		try:
			response = requests.get(url)
			response.raise_for_status()
			return response.json()
		except Exception as e:
			raise HoyoDLException(self.errors["jsonError"].format(e))

		return None

	def _isGameValid(self, game: str | None) -> bool:
		if not game:
			return False
		return game in self.data

	def _isVersionValid(self, version: str | None) -> bool:
		if not version:
			return False
		return version in self.data[self.game]["hashes"] and version >= self.data[self.game]["minVersion"]

	def _isGameVersionValid(self) -> bool:
		return self._isGameValid(self.game) and self._isVersionValid(self.version)

	def _setupCheck(self) -> None:
		if not self._isGameVersionValid():
			raise HoyoDLException(self.errors["incompleteSetup"])

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

	def _filteredFilesBase(self, base: str) -> list:
		res = []

		for file in self.filesIndex:
			if file["name"].startswith(self.data[self.game]["filesIndexOptions"][base]):
				res.append(file)

		return res

	######################
	### Update configs ###
	######################

	def setGame(self, game: str) -> None:
		if not self._isGameValid(game):
			raise HoyoDLException(self.errors["invalidGame"].format(", ".join(self.data.keys())))
		self.game = game
		self.version = None
		self.filesIndex.clear()

	def setVersion(self, version: str) -> None:
		if not self.game:
			raise HoyoDLException(self.errors["noGame"])
		if not self._isVersionValid(version):
			raise HoyoDLException(self.errors["invalidVersion"].format(self.data[self.game]["minVersion"], list(self.data[self.game]["hashes"].keys())[-1]))
		self.version = version
		self.filesIndex.clear()

	#####################
	### Get functions ###
	#####################

	def getHash(self) -> str:
		self._setupCheck()
		return self.data[self.game]["hashes"][self.version]

	def getLatestVersion(self) -> str:
		if not self._isGameValid(self.game):
			raise HoyoDLException(self.errors["noGame"])
		return list(self.data[self.game]["hashes"].keys())[-1]

	def getReleaseDate(self, raw: bool=False) -> str:
		self._setupCheck()
		_hash = self.getHash()
		timestamp = _hash.split("_")[0]
		if raw:
			return timestamp
		dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
		day = dt.day
		suffix = "th" if 11 <= dt.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(dt.day % 10, "th")
		return f"{dt.strftime('%B')} {day}{suffix}, {dt.year} at {dt.strftime('%H:%M:%S')}"

	def getFileURL(self, path: str) -> str:
		self._setupCheck()
		data = self.data[self.game]
		url = f'{data["scatterURL"].replace("$0", data["hashes"][self.version])}/{path}'
		return url

	###################
	### Files index ###
	###################

	def getAllBlockFiles(self) -> list:
		self._setupCheck()
		self._fetchFilesIndex()
		blocks = self._filteredFilesBase("blocksRef")
		return blocks

	def getAllAudioFiles(self) -> list:
		self._setupCheck()
		self._fetchFilesIndex()
		files = self._filteredFilesBase("audioRef")
		return files

	def getAllCutscenesFiles(self) -> list:
		self._setupCheck()
		self._fetchFilesIndex()
		files = self._filteredFilesBase("cutscenesRef")
		return files

	##########################
	### Download functions ###
	##########################

	def downloadBlock(self, id: str):
		self._setupCheck()
		data = self.data[self.game]
		ref = f'{data["blocksRef"]}/{id}.{data["blocksFormat"]}'
		url = self.getFileURL(ref)
		return self._downloadInstance(url)

	def downloadFile(self, path: str):
		self._setupCheck()
		url = self.getFileURL(path)
		return self._downloadInstance(url)

class HoyoDLException(Exception):
	def __init__(self, message):
		super().__init__(message)
