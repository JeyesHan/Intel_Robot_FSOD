import os
import sys
import json
import shutil

filter_json_file = sys.argv[1]
with open(filter_json_file, 'r') as f:
    filter_img_ids = json.load(f)
for img_id in filter_img_ids:
    src_path = os.path.join('/home/hanj/pyprojects/robot_initial/labelme_images/no_label_images', img_id+'.json')
    dst_path = os.path.join('labelme_images/images', img_id+'.json')
    shutil.copy(src_path, dst_path)