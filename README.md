# Few-Shot Object Detection WorkFlow
## Training Procedure
### Step1, extract frames from three videos
```
ffmpeg -i 1.mp4 1/1%04d.jpg
ffmpeg -i 2.mp4 2/2%04d.jpg
ffmpeg -i 3.mp4 3/33%04d.jpg
```

### Step2, annotate 3 instances using labelme
```
# In your local laptop, annotate
labelme data_annotated --labels labels.txt --nodata --autosave
```

### Step3, formulate voc-like dataset
```
step=0
DIR_PREFIX=/home/hanj/pyprojects
cd ${DIR_PREFIX}/labelme/examples/bbox_detection
./labelme2voc.py ${DIR_PREFIX}/robot_initial/labelme_images/images ${DIR_PREFIX}/robot_initial/step${step} --labels ${DIR_PREFIX}/robot_initial/labelme_images/labels.txt
python gen_splits.py ${DIR_PREFIX}/robot_initial/step${step}
```
### Step4, finetume detector on annotate images
*You should first set proper finetune iterations in config file*
```
cd ${DIR_PREFIX}/DeFRCN_smog
sh run_robot_competition.sh robot_competition_step${step}
```

### Step5, inference on remain images
```
python gen_vis_pseudo_anno.py --output ${DIR_PREFIX}/robot_initial/vis_step${step} --weights ${DIR_PREFIX}/DeFRCN_smog/checkpoints/voc/robot_competition_step${step}/defrcn_fsod_r101_novel/fsrw-like/10shot_seed0_repeat0/model_final.pth
```
After that, download ```${DIR_PREFIX}/robot_initial/vis_step${step}``` to local desktop, select reliable samples to enlarge the training set.


```
cd ${DIR_PREFIX}/robot_initial
rm -rf labelme_images/images && cp -r labelme_images/images_bk labelme_images/images
```
### Optional Step, augment data by Stitching images
We stitch images randomly to reduce the over-reliance on background when detecting objects.
```
cd ${DIR_PREFIX}/robot_initial
python stitching_images.py ${DIR_PREFIX}/robot_initial/labelme_images/images ${DIR_PREFIX}/robot_initial/labelme_images/aug_images 100
mv ${DIR_PREFIX}/robot_initial/labelme_images/aug_images/* ${DIR_PREFIX}/robot_initial/labelme_images/images
```
### Step6, select reliable pseudo labels to form new train set
```
python move_pseudo_json.py ${DIR_PREFIX}/robot_initial/filter_vis_step${step}.json
# Enlarge the setp pointer
step=xx
cd ${DIR_PREFIX}/labelme/examples/bbox_detection
./labelme2voc.py ${DIR_PREFIX}/robot_initial/labelme_images/images ${DIR_PREFIX}/robot_initial/step${step} --labels ${DIR_PREFIX}/robot_initial/labelme_images/labels.txt
python gen_splits.py ${DIR_PREFIX}/robot_initial/step${step}
cd ${DIR_PREFIX}/robot_initial
rm -rf stepx
ln -s step${step} stepx
```
### Step7, repeat Step4-Step6


# Robot Offline Test
```
cd ${DIR_PREFIX}/DeFRCN_smog
python robot_test.py --input ${DIR_PREFIX}/robot_test/JPEGImages --output ${DIR_PREFIX}/robot_test_vis --weights ${DIR_PREFIX}/DeFRCN_smog/checkpoints/voc/robot_competition_step${step}/defrcn_fsod_r101_novel/fsrw-like/10shot_seed0_repeat0/model_0001999.pth
```

# Finetune Steps
|  Step   | 1  | 2|3|>=4|
|  ---- | ----|---|---|---|
| # Img  | 3 |x|~200|>=220|
| iter1  | 400 |2400|3200|6400
| iter2  | 500 |3000|4000|8000