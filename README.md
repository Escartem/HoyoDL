# HoyoDL

Download any file at any version from Hoyo games, with additional utilities.

## Setting up

First, create an instance of the class :

```py
>>> import HoyoDL
>>> client = HoyoDL(game="hk4e", version="5.5")
```

You can also specify the game and version separately :

```py
>>> client = HoyoDL()
>>> client.setGame("hk4e")
>>> client.setVersion("5.4")
```

The list of games is as follow :

| Game | Game ID | Minimum supported version |
| - | - | - |
| Genshin Impact | `hk4e` | 2.3 |
| Honkai: Star Rail | `hkrpg` | 1.5 |
| Zenless Zone Zero | `nap` | 1.1 |

## Downloading a file

To download a file, call `downloadFile()` and specify its path, the game and version must be defined :

```py
>>> dl = client.downloadFile("GenshinImpact.exe")
>>> dl = client.downloadFile("GenshinImpact_Data/app.info")
```

This functions returns a `requests.Response` object, you can then use it to save your file :

```py
>>> file = "GenshinImpact.exe"
>>> dl = client.downloadFile(file)
>>>
>>> with open(file, "wb") as f:
>>>     f.write(dl.content)
```

Or if you want to have a progress along with it, save it in chunks :

```py
>>> file = "GenshinImpact.exe"
>>> dl = client.downloadFile(file)
>>> 
>>> with open(file, "wb") as f:
>>> 	for chunk in dl.iter_content(chunk_size=8192): # use chunk size of your choice
>>> 		f.write(chunk)
```

The tool also provides a shortcut function to download a block file using `downloadBlock()`, this functions returns a `requests.Response` object too :

```py
>>> client = HoyoDL(game="hkrpg", version="3.1")
>>> block = "000a8acede9ed8aea7a8c3281a2f7ebd" # file extension is automatically added upon request as it differs between games
>>> dl = client.downloadBlock(block) # will download 000a8acede9ed8aea7a8c3281a2f7ebd.block
```

⚠️ Genshin uses folders for blocks, so you must add the folder name in the block name to download correctly :

```py
>>> client = HoyoDL(game="hk4e", version="5.5")
>>> block = "00/35323818"
>>> dl = client.downloadBlock(block) # will download 00/35323818.blk
```

If you don't want to have a `requests.Response` object but rather a URL directly, you can use `getFileURL()` instead :

```py
>>> client = HoyoDL(game="hk4e", version="5.5")
>>> url = client.getFileURL("GenshinImpact.exe")
>>> print(url)
"https://autopatchhk.yuanshen.com/client_app/download/pc_zip/20250314110016_HcIQuDGRmsbByeAE/ScatteredFiles/GenshinImpact.exe"
```

## Getting files names

If you don't know what files you can have, or want to get lists easily, you can call the following functions, each will return a list of files, each file being a dictionary in the following structure :

```
{
  "name": "path/to/file.ext",
  "md5": "md5 hash",
  "size": "size in bytes"
}
```

To get all blocks :

```py
>>> files = client.getAllBlockFiles()
>>> dl = client.downloadFile(files[0]["name"])
```

To get all audio files :

```py
>>> files = client.getAllAudioFiles()
```

To get all cutscenes files :

```py
>>> files = client.getAllCutscenesFiles()
```

ℹ️ When running any of these functions for the first time may take a few additional seconds as the tool is fetching the list, afterwards it will be cached for future calls until the game or version is changed

## Getting miscellaneous information

After selecting a game and version, you can get the date of when this version was released to the servers :

```py
>>> client = HoyoDL(game="hk4e", version="2.7")
>>> date = client.getReleaseDate()
>>> print(date)
"April 29th, 2022 at 11:24:15"
```

You can also get the timestamp directly if you don't want the formatted date, the output will be in the form `YYYYmmddHHMMSS` :

```py
>>> date = client.getReleaseDate(raw=True)
>>> print(date)
20220429112415
```

You can also get the version hash if necessary :

```py
>>> hash = client.getHash()
>>> print(hash)
"20220429112415_dDweiEHDnBI6cKmM"
```

## Customizing the data

This tool works by using what is called a provider json file, this file contains all the games, versions and hashes for each version, the default file is hosted [here](https://ena.escartem.moe/hoyodl/data.json), but you may want to also make your own to add custom games or add missing version (in case I forget to add the latest ones for example)

To do so, create a json file in the same structure as the official one, host it wherever you want and pass the url to it when initializing the tool :

```py
>>> client = HoyoDL(provider="https://example.com/path/file.json")
```

## Contributing

Any help or contributions to this tool are greatly appreciated, or, if this helped you, a star is also welcome （＾∀＾●）ﾉｼ
