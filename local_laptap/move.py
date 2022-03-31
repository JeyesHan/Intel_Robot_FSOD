import os
import sys
import json
import shutil


step = int(sys.argv[1])
prev = str(step-1)
step = str(step)

src = 'vis_step' + step
dst = 'filter_vis_step' + step
if os.path.isdir(dst):
    shutil.rmtree(dst)
os.makedirs(dst)
with open('filter_vis_step%s.json'% prev, 'r') as f:
    img_ids = json.load(f)
for img_id in img_ids:
    shutil.move(os.path.join(src, img_id+'.jpg'), os.path.join(dst, img_id+'.jpg'))
