######## Webcam Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 1/20/18
# Description:
# This program uses a TensorFlow-trained classifier to perform object detection.
# It loads the classifier uses it to perform object detection on a webcam feed.
# It draws boxes and scores around the objects of interest in each frame from
# the webcam.

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

## but I changed it to make it more understandable to me.


# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util


# 追加
import collections

# CSV
import csv
import pprint

import datetime
dt_now = datetime.datetime.now()

# from utils import backbone
# from api import object_counting_api

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 3

## Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Initialize webcam feed
video = cv2.VideoCapture(0)
ret = video.set(3,1280)
ret = video.set(4,720)

skippers_num = 0
swallowtail_num = 0
whitebutterfly_num = 0

skippers_sum = 0
swallowtail_sum = 0
whitebutterfly_sum = 0

skippers_prev = 0
swallowtail_prev = 0
whitebutterfly_prev = 0

countFlg_skippers = False
countFlg_swallowtail = False
countFlg_whitebutterfly = False

while(True):

    # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    ret, frame = video.read()
    frame_expanded = np.expand_dims(frame, axis=0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})

    # Draw the results of the detection (aka 'visulaize the results')
    vis_util.visualize_boxes_and_labels_on_image_array(
        frame,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.60)

    # All the results have been drawn on the frame, so it's time to display it.
    cv2.imshow('Object detector', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):

        # test code for writing butterfly sum on CSV file

        data = str(dt_now.year)+':'+str(dt_now.month)+':'+str(dt_now.day)

        with open('Object_detection_xlab/data/sample_writer.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([data, skippers_sum, swallowtail_sum, whitebutterfly_sum])

        with open('Object_detection_xlab/data/sample_writer.csv') as f:
            print(f.read())

        break

    # for index,value in enumerate(classes[0]):
    #     if scores[0,index] > 0.60:
    #         print(category_index.get(value))

    count_num = [category_index.get(value)['name'] for index,value in enumerate(classes[0]) if scores[0,index] > 0.60]
    c = collections.Counter(count_num)

    # skippers_sum += skippers_num
    # swallowtail_sum += swallowtail_num
    # whitebutterfly_sum += whitebutterflu_num

    #count skippers
    if skippers_num == 0:
        print('no butterfly')

    elif skippers_num !=0 and skippers_num > skippers_prev:
        countFlg_skippers = True
        print('a few butterflies appeared')

    if countFlg_skippers == True:
        skippers_sum = skippers_sum + (skippers_num-skippers_prev)

    countFlg_skippers = False
    skippers_prev = skippers_num

    #count swallowtail
    if swallowtail_num == 0:
        print('no butterfly')

    elif swallowtail_num !=0 and swallowtail_num > swallowtail_prev:
        countFlg_swallowtail = True
        print('a few butterflies appeared')

    if countFlg_swallowtail == True:
        swallowtail_sum = swallowtail_sum + (swallowtail_num-swallowtail_prev)

    countFlg_swallowtail = False
    swallowtail_prev = swallowtail_num

    #count whitebutterfly
    if whitebutterfly_num == 0:
        print('no butterfly')

    elif whitebutterfly_num !=0 and whitebutterfly_num > whitebutterfly_prev:
        countFlg_whitebutterfly = True
        print('a few butterflies appeared')

    if countFlg_whitebutterfly == True:
        whitebutterfly_sum = whitebutterfly_sum + (whitebutterfly_num-whitebutterfly_prev)

    countFlg_whitebutterfly = False
    whitebutterfly_prev = whitebutterfly_num

    # print(c.most_common())
    skippers_num = count_num.count('skippers')
    swallowtail_num = count_num.count('swallowtail')
    whitebutterfly_num = count_num.count('whitebutterfly')

    print('skippers:')
    print(str(skippers_num)+', '+str(skippers_sum))
    print('swallowtail:')
    print(str(swallowtail_num)+', '+str(swallowtail_sum))
    print('whitebutterfly:')
    print(str(whitebutterfly_num)+', '+str(whitebutterfly_sum))

# Clean up
video.release()
cv2.destroyAllWindows()
