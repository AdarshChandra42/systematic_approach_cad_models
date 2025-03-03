import os
import cv2
import numpy as np
import tensorflow as tf
import sys

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = '../TensorFlow/trained-inference-graphs/output_inference_graph_vAGAIN.pb'

path = '/home/igor/Documentos/Developments/Experiment_Plan/Renault_Oficial_Images/ad_blue_all'

PATH_TO_IMAGE = []
IMAGE = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.png' in file:
            PATH_TO_IMAGE.append(os.path.join(r, file))
            IMAGE.append(file)

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'../TensorFlow/annotations','label_map.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 1

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


# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objectbresil_ad_blue4_0.pngs.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# width = 705, height = 447
# width = 2590, height = 1942
largura = 2590
altura = 1942

pred_labels_list = []
for f in IMAGE:
    path_to_img = os.path.join(path,f)
    image = cv2.imread(path_to_img)
    image_expanded = np.expand_dims(image, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    ymin = boxes[0,0,0] * altura
    xmin = boxes[0,0,1] * largura
    ymax = boxes[0,0,2] * altura
    xmax = boxes[0,0,3] * largura

    value_pred = [f, xmin, ymin, xmax, ymax]
    pred_labels_list.append(value_pred)
    print(value_pred)

pred_labels_list.sort()
print("\n")

for i in pred_labels_list:
    print(i)
