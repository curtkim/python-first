import logging
import os
import pathlib
import xml.etree.ElementTree as ET

import cv2
import numpy as np
from numpy import random


class VOCDataset:

    def __init__(self, root=None, image_sets_file=None, transform=None, target_transform=None, is_test=False,
                 keep_difficult=False, label_fn='vision/datasets/TLR_labels_compact.txt', verbos = False):
        """Dataset for VOC data.
        Args:
            root: the root of the VOC2007 or VOC2012 dataset, the directory contains the following sub-directories:
                Annotations, ImageSets, JPEGImages, SegmentationClass, SegmentationObject.
            image_sets_file : eg. "root/ImageSets/Main/trainval.txt". if ImageSet_file is not None, root, image_sets_file are overwrited from ImageSet_file infor
        """
        if image_sets_file is not None:
            root, fn = os.path.split(image_sets_file)
            root, fn = os.path.split(root)
            root, fn = os.path.split(root)

        self.root = pathlib.Path(root) if root is not None else None
        self.transform = transform
        self.target_transform = target_transform
        if (image_sets_file is None) and (self.root is not None):
            if is_test:
                image_sets_file = self.root / "ImageSets/Main/test.txt"
            else:
                image_sets_file = self.root / "ImageSets/Main/trainval.txt"
        self.ids = VOCDataset._read_image_ids(image_sets_file)
        self.keep_difficult = keep_difficult

        # if the labels file exists, read in the class names
        self.label_fn = label_fn
        self.verbos = verbos

        # parsing and reading label file :
        text_file = open(label_fn, "r")
        lines = text_file.read().split('\n')
        if lines[-1] == '': lines = lines[:-1]
        class_names_etri = [line.split(' ')[0] for line in lines]
        class_colors = [list(map(int, line.split(' ')[1:4])) for line in lines]
        class_names_kakao = [line.split(' ')[4] for line in lines]
        class_names_training = [line.split(' ')[5] for line in lines]
        nms_ignore_class = [line.split(' ')[6] for line in lines]

        # object name converting
        self.class_name_convert_to_trainingName = {}
        self.class_name_convert_to_trainingName.update(
            {class_name: class_names_training[i] for i, class_name in enumerate(class_names_training)})
        self.class_name_convert_to_trainingName.update(
            {class_name: class_names_training[i] for i, class_name in enumerate(class_names_etri)})
        self.class_name_convert_to_trainingName.update(
            {class_name: class_names_training[i] for i, class_name in enumerate(class_names_kakao)})
        self.class_name_convert_to_trainingName_keys = self.class_name_convert_to_trainingName.keys()


        # make class_names, colors, nms_ignore
        self.class_colors = []
        self.class_names = []
        self.nms_ignore_class = []
        for i, class_name in enumerate(class_names_training):
            if (class_name in self.class_names) is False:
                self.class_names.append(class_name)
                self.nms_ignore_class.append(nms_ignore_class[i])
                self.class_colors.append(class_colors[i])

        self.class_dict = {class_name: i for i, class_name in enumerate(self.class_names)}
        nclass = len(self.class_dict)


    def __getitem__(self, index):
        while True:
            image_id = self.ids[index]
            boxes, labels, is_difficult = self._get_annotation(image_id)

            # difficulty filtering
            if boxes.shape[0] > 0:
                if not self.keep_difficult:
                    boxes = boxes[is_difficult == 0]
                    labels = labels[is_difficult == 0]

            # bbox가 없는 이미지는 사용하지 않는다.
            if boxes.shape[0] == 0:
                #index += 1
                index += random.randint(len(self.ids))
                index %= len(self.ids)
            else:
                break

        status, image = self._read_image(image_id)
        assert(status, "Fail in _read_image() with "+str(image_id))

        ## check bbox boundary
        h,w,d  = image.shape
        boxes[boxes[:, 0] < 0, 0] = 0
        boxes[boxes[:, 1] < 0, 1] = 0
        boxes[boxes[:, 2] >=w, 2] = w-1
        boxes[boxes[:, 3] >=h, 3] = h-1

        if self.transform:
            image, boxes, labels = self.transform(image, boxes, labels)
        if self.target_transform:
            boxes, labels = self.target_transform(boxes, labels)
        return image, boxes, labels


    def get_color(self, label):
        """ Color for bounding box visualization
        Returns:
          Color-Vector (BGR) for traffic light visualization
        """
        return self.class_colors( self.class_dict[label])

    def get_color_idx(self, idx):
        """ Color for bounding box visualization
        Returns:
          Color-Vector (BGR) for traffic light visualization
        """
        return self.class_colors[idx]

    def get_image(self, index):
        image_id = self.ids[index]
        status, image = self._read_image(image_id)
        if status:
            if self.transform:
                image, _ = self.transform(image)
        return status, image

    def get_annotation(self, index):
        image_id = self.ids[index]
        return image_id, self._get_annotation(image_id)

    def __len__(self):
        return len(self.ids)

    @staticmethod
    def _read_image_ids(image_sets_file):
        ids = []
        if image_sets_file is None:
            return ids
        with open(image_sets_file) as f:
            for line in f:
                ids.append(line.rstrip())
        return ids

    def write_annotation(self, image_fn_path, label_indexes, bndboxes, probs, folder_name=None, width=None, height=None, depth=None):
        # image_fn_path : file name
        # label_indexes : name = self.class_names[label_indexes[i]]
        # probs : float

        path, image_fn = os.path.split(image_fn_path)
        xml_fn_path = os.path.join(path, image_fn[:-3] + "xml")

        with open(xml_fn_path, "w") as f:
            f.write("<annotation>\n")
            f.write("  <filename>"+image_fn+"</filename>\n")
            if folder_name is not None:
                f.write("  <folder>"+folder_name+"</folder>\n")
            if width is not None:
                f.write("  <size>\n    <width>"+str(width)+"</width>\n    <height>"+str(height)+"</height>\n    <depth>"+str(depth)+"</depth>\n  </size>\n")
            f.write("  <segmented>0</segmented>\n")
            f.write("  <autolabel>1</autolabel>\n")
            for i, label_index in enumerate(label_indexes):
                f.write("  <object>\n")
                f.write("    <name>"+self.class_names[label_indexes[i]]+"</name>\n")
                f.write("    <bndbox>\n")
                f.write("      <xmin>"+str(int(0.5+bndboxes[i][0]))+"</xmin>\n")
                f.write("      <ymin>"+str(int(0.5+bndboxes[i][1]))+"</ymin>\n")
                f.write("      <xmax>"+str(int(0.5+bndboxes[i][2]))+"</xmax>\n")
                f.write("      <ymax>"+str(int(0.5+bndboxes[i][3]))+"</ymax>\n")
                f.write("    </bndbox>\n")
                f.write("    <probs>"+str(probs[i].item())+"</probs>\n")
                f.write("  </object>\n")
            f.write("</annotation>\n")

    def _get_annotation(self, image_id):
        annotation_file = self.root / f"Annotations/{image_id}.xml"
        boxes = []
        labels = []
        is_difficult = []

        if os.path.isfile(annotation_file) is False:
            if self.verbos :    print("annotation_file " + str(annotation_file) + "not found")

        elif os.path.getsize(annotation_file) == 0:
            if self.verbos :    print('annotation file is empty : '+annotation_file)

        else:
            objects = ET.parse(annotation_file).findall("object")

            if len(objects) > 0 and objects[0].text is not None:
                if len(objects[0].findall('item')) > 0: # AIMMO dataset 은 object / item / name 순으로 되어 있음
                    objects = objects[0].findall('item')

                for object in objects:
                    #class_name = object.find('name').text.lower().strip()
                    class_name_raw = object.find('name').text.strip()

                    if class_name_raw not in self.class_name_convert_to_trainingName_keys:
                        print('(skip) class_name, %s, is not in class_name_convert_to_trainingName_keys'%class_name_raw)
                        continue
                    class_name = self.class_name_convert_to_trainingName[class_name_raw]
                    # we're only concerned with clases in our list
                    if class_name in self.class_dict:
                        bbox = object.find('bndbox')

                        # VOC dataset format follows Matlab, in which indexes start from 0
                        x1 = float(bbox.find('xmin').text) - 1
                        y1 = float(bbox.find('ymin').text) - 1
                        x2 = float(bbox.find('xmax').text) - 1
                        y2 = float(bbox.find('ymax').text) - 1
                        boxes.append([min(x1, x2), min(y1,y2), max(x1,x2), max(y1,y2)])
                        is_small = True if min(abs(x2-x1), abs(y2-y1))<=4 else False

                        labels.append(self.class_dict[class_name])
                        is_difficult_str = object.find('difficult')
                        is_difficult.append(int(is_difficult_str.text) if is_difficult_str else is_small)

        return (np.array(boxes, dtype=np.float32),
                np.array(labels, dtype=np.int64),
                np.array(is_difficult, dtype=np.uint8))

    def _read_image(self, image_id):
        image_file = self.root / f"JPEGImages/{image_id}.jpg"
        return self._read_image_from_filename(image_file)

    def _read_image_from_filename(self, file_name):
        if os.path.isfile(file_name):
            image = cv2.imread(str(file_name), cv2.IMREAD_UNCHANGED)
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return True, image
        else:
            print("Image " + str(file_name) + " not found")
            return False, []


def test_VOCDataset():

    dataset = VOCDataset(image_sets_file='/data/datasets/omega-tlr/pangyo_front_main/ImageSets/Main/all.txt',
                         label_fn='/data/datasets/omega-tlr/TLR_labels_compact.txt')
    nSample = dataset.__len__()
    print("# of sample : "+str(nSample))

    import matplotlib.pyplot as plt
    from PIL import Image

    #cv2.namedWindow('image')
    #cv2_wait_val = 0

    nboxes = 0
    for i in range(nSample):
        image, boxes, labels = dataset.__getitem__(i)
        print(i, image.shape, boxes, labels)
        # image.shape
        # (1080, 1920, 3)
        # boxes
        # [[801. 439. 815. 500.]
        #  [405. 449. 423. 518.]
        #  [145. 273. 214. 308.]
        #  [  0. 249.  62. 288.]]
        # labels
        # [17 15  2  2]
        nboxes += boxes.shape[0]

        #cv2.imshow('image', image)
        #cv2.waitKey(cv2_wait_val)

    print("# of boxes : "+str(nboxes))
    #cv2.destroyAllWindows()


if __name__ == '__main__':
    test_VOCDataset()
