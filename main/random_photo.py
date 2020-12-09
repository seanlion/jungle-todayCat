from main import *

files=os.listdir(BOARD_IMAGE_PATH)
print(files)
d=random.choice(files)
print("d:",d)