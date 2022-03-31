import os
import sys
import json

data_root = sys.argv[1]
img_ids = []
for img_name in os.listdir(data_root):
    if img_name.endswith('.jpg'):
        img_ids.append(img_name[:-4])
with open(data_root+'.json', 'w') as f:
    json.dump(img_ids, f, indent=1)