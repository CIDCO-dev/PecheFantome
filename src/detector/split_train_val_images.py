import os
import shutil

notEmptyFiles = []
emptyFiles = []

with os.scandir("/data/dataset/Ghost_Gear/data/labels") as dir:
	for file in dir:
		#print(file)
		if not os.path.getsize(file) == 0:
			notEmptyFiles.append(file.name)
		else:
			emptyFiles.append(file.name)


valAmount =  int(20/100 * len(notEmptyFiles))
valAmountEmpties = int(10/100 * len(emptyFiles))

for i in range(len(notEmptyFiles)):
	filename = notEmptyFiles[i]
	filename = filename.replace(filename[len(filename)-4:],".jpg")
	notEmptyFiles[i] = filename

for i in range(len(emptyFiles)):
	filename = emptyFiles[i]
	filename = filename.replace(filename[len(filename)-4:],".jpg")
	emptyFiles[i] = filename


filesToMove = notEmptyFiles[:valAmount] + emptyFiles[:valAmountEmpties]


print(len(filesToMove))
print(valAmount + valAmountEmpties)

srcPath = "/data/dataset/Ghost_Gear/data/images"
dstPath = "/data/dataset/Ghost_Gear/data/val"

for f in filesToMove:
	src = os.path.join(srcPath, f)
	if os.path.exists(src):
		shutil.move(src, dstPath)
