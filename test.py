from HoyoDL import HoyoDL

test = HoyoDL()
test.setGame("hk4e")
test.setVersion("5.5")

print(test.getReleaseDate())

file = "GenshinImpact.exe"
dl = test.downloadFile(file)

# with open(file, "wb") as f:
# 	for chunk in dl.iter_content(chunk_size=8192):
# 		f.write(chunk)

block = "00/35323818"
dl = test.downloadBlock(block)

# with open(block, "wb") as f:
# 	for chunk in dl.iter_content(chunk_size=8192):
# 		f.write(chunk)

# with open(block, "wb") as f:
#     f.write(dl.content)

print(test.getAllCutscenesFiles())

test.setGame("nap")
test.setVersion("1.5")

print(test.getAllCutscenesFiles())
# test._fetchFilesIndex()
# print(test.filesIndex)