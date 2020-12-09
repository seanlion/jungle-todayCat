from main import os,random,BOARD_IMAGE_PATH

files=os.listdir(BOARD_IMAGE_PATH)
print(files)
d=random.choice(files)
print("d:",d)