# HoyoDL

Download any file at any version from Hoyo games, with additional utilities.

## Usage

First create an instance of the class

```py
>>> import HoyoDL
>>> client = HoyoDL(game="hk4e", version="5.5")
```

You can also specify the game and version separately

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

To download a file, call `downloadFile()` and specify its path, the game and version must be defined.

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
