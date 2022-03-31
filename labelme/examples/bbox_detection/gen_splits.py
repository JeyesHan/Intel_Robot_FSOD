import os
import sys


data_root = sys.argv[1]
trainval_ratio = 0.8
ext = 'jpg'

image_ids = []
for img in os.listdir(os.path.join(data_root, 'JPEGImages')):
    if not img.endswith(ext):
        continue
    image_ids.append(img[:-(len(ext)+1)])

train_ids = image_ids # [:int(len(image_ids)*trainval_ratio)]
val_ids = image_ids # [int(len(image_ids)*trainval_ratio):]

if not os.path.isdir(os.path.join(data_root, 'ImageSets/Main')):
    os.makedirs(os.path.join(data_root, 'ImageSets/Main'))

with open(os.path.join(data_root, 'ImageSets/Main/trainval.txt'), 'w') as f:
    train_ids = [item + '\n' for item in train_ids]
    f.writelines(train_ids)

with open(os.path.join(data_root, 'ImageSets/Main/test.txt'), 'w') as f:
    val_ids = [item + '\n' for item in val_ids]
    f.writelines(val_ids)    
