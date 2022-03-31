import os
import shutil
import cv2
import glob
import json
import sys
import numpy as np

class Mosaic:
    def __init__(self, img_ids, img_data_dict, img_anno_dict) -> None:
        self.img_ids = img_ids
        self.img_data_dict = img_data_dict
        self.img_anno_dict = img_anno_dict

    def box2json(self, img, img_ids, boxes, classes):
        ret = {"version": "5.0.1", "flags": {}, "shapes": [], "imageData": None,}
        ret["imagePath"] = '_'.join(img_ids) + '.jpg'
        ret["imageHeight"], ret["imageWidth"], _ = img.shape

        for i, (box, cls) in enumerate(zip(boxes, classes)):
            ret["shapes"].append({
                "label": cls,
                "points": [
                    [box[0], box[1]],
                    [box[2], box[3]]
                ],
                "group_id": None,
                "shape_type": "rectangle",
                "flags": {}
            })
        return ret

    def duble_column(self, ):
        select_img_ids = np.random.choice(self.img_ids, 2, replace=False)
        img_id1, img_id2 = select_img_ids
        img1, img2 = self.img_data_dict[img_id1], img_data_dict[img_id2]
        box1, class1 = np.array(self.img_anno_dict[img_id1]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id1]['shapes'][0]['label']
        box2, class2 = np.array(self.img_anno_dict[img_id2]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id2]['shapes'][0]['label']
        h, w, c = img1.shape
        new_img = np.concatenate((img1, img2), 1)
        
        new_box2 = box2[:]
        new_box2[0] += w
        new_box2[2] += w
        new_boxes = [box1, new_box2]
        new_classes = [class1, class2]
        return new_img, self.box2json(new_img, select_img_ids, new_boxes, new_classes)

    def triple_column(self, ):
        select_img_ids = np.random.choice(self.img_ids, 3, replace=False)
        img_id1, img_id2, img_id3 = select_img_ids
        img1, img2, img3 = self.img_data_dict[img_id1], img_data_dict[img_id2], img_data_dict[img_id3]
        box1, class1 = np.array(self.img_anno_dict[img_id1]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id1]['shapes'][0]['label']
        box2, class2 = np.array(self.img_anno_dict[img_id2]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id2]['shapes'][0]['label']
        box3, class3 = np.array(self.img_anno_dict[img_id3]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id3]['shapes'][0]['label']
        h, w, c = img1.shape
        new_img = np.concatenate((img1, img2, img3), 1)
        
        new_box2 = box2[:]
        new_box2[0] += w
        new_box2[2] += w

        new_box3 = box3[:]
        new_box3[0] += 2 * w
        new_box3[2] += 2 * w
        new_boxes = [box1, new_box2, new_box3]
        new_classes = [class1, class2, class3]
        return new_img, self.box2json(new_img, select_img_ids, new_boxes, new_classes)

    def grid(self, ):
        select_img_ids = np.random.choice(self.img_ids, 4, replace=False)
        img_id1, img_id2, img_id3, img_id4 = select_img_ids
        img1, img2, img3, img4 = self.img_data_dict[img_id1], img_data_dict[img_id2], img_data_dict[img_id3], img_data_dict[img_id4]
        box1, class1 = np.array(self.img_anno_dict[img_id1]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id1]['shapes'][0]['label']
        box2, class2 = np.array(self.img_anno_dict[img_id2]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id2]['shapes'][0]['label']
        box3, class3 = np.array(self.img_anno_dict[img_id3]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id3]['shapes'][0]['label']
        box4, class4 = np.array(self.img_anno_dict[img_id4]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id4]['shapes'][0]['label']
        h, w, c = img1.shape
        tmp1 = np.concatenate((img1, img2), 1)
        tmp2 = np.concatenate((img3, img4), 1)
        new_img = np.concatenate((tmp1, tmp2), 0)
        
        new_box2 = box2[:]
        new_box2[0] += w
        new_box2[2] += w

        new_box3 = box3[:]
        new_box3[1] += h
        new_box3[3] += h

        new_box4 = box4[:]
        new_box4[0] += w
        new_box4[1] += h
        new_box4[2] += w
        new_box4[3] += h
        new_boxes = [box1, new_box2, new_box3, new_box4]
        new_classes = [class1, class2, class3, class4]
        return new_img, self.box2json(new_img, select_img_ids, new_boxes, new_classes)

    def non_grid(self, ):
        select_img_ids = np.random.choice(self.img_ids, 3, replace=False)
        img_id1, img_id2, img_id3 = select_img_ids
        img1, img2, img3 = self.img_data_dict[img_id1], img_data_dict[img_id2], img_data_dict[img_id3]
        box1, class1 = np.array(self.img_anno_dict[img_id1]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id1]['shapes'][0]['label']
        box2, class2 = np.array(self.img_anno_dict[img_id2]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id2]['shapes'][0]['label']
        box3, class3 = np.array(self.img_anno_dict[img_id3]['shapes'][0]['points']).reshape(-1), self.img_anno_dict[img_id3]['shapes'][0]['label']
        h, w, c = img1.shape
        img2 = cv2.resize(img2, (w//2, h//2))
        img3 = cv2.resize(img3, (w//2, h//2))
        
        tmp1 = np.concatenate((img2, img3), 0)
        new_img = np.concatenate((img1, tmp1), 1)
        
        new_box2 = box2[:]
        new_box2[0] = new_box2[0] // 2 + w
        new_box2[1] = new_box2[1] // 2
        new_box2[2] = new_box2[2] // 2 + w
        new_box2[3] = new_box2[3] // 2

        new_box3 = box3[:]
        new_box3[0] = new_box3[0] // 2 + w
        new_box3[1] = new_box3[1] // 2 + h // 2
        new_box3[2] = new_box3[2] // 2 + w
        new_box3[3] = new_box3[3] // 2 + h // 2
        new_boxes = [box1, new_box2, new_box3]
        new_classes = [class1, class2, class3]
        return new_img, self.box2json(new_img, select_img_ids, new_boxes, new_classes)

if __name__ == '__main__':
    data_root = sys.argv[1] # '/home/hanj/pyprojects/robot_initial/labelme_images/images'
    save_dir = sys.argv[2] # '/home/hanj/pyprojects/robot_initial/labelme_images/aug_images'
    n = int(sys.argv[3])

    if os.path.isdir(save_dir):
        shutil.rmtree(save_dir)
    os.makedirs(save_dir)
    img_ids = []
    for item in os.listdir(data_root):
        if item.endswith('.json'):
            img_ids.append(item.split('.')[0])

    img_data_dict = {}
    img_anno_dict = {}
    for img_id in img_ids:
        img = cv2.imread(os.path.join(data_root, img_id+'.jpg'))
        with open(os.path.join(data_root, img_id+'.json'), 'r') as f:
            img_anno = json.load(f)
        img_data_dict[img_id] = img
        img_anno_dict[img_id] = img_anno

    mosaic_aug = Mosaic(img_ids, img_data_dict, img_anno_dict)

    for i in range(n):
        aug_choices = ['duble_column', 'triple_column', 'grid', 'non_grid']
        choosed_aug = np.random.choice(aug_choices, 1)[0]
        new_img, anno = getattr(mosaic_aug, choosed_aug)()
        anno['imagePath'] = choosed_aug + '_' + anno['imagePath']
        cv2.imwrite(os.path.join(save_dir, anno['imagePath']), new_img)
        with open(os.path.join(save_dir, anno['imagePath'].replace('.jpg', '.json')), 'w') as f:
            json.dump(anno, f, indent=1)
