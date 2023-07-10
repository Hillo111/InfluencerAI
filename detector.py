import cv2
import argparse
import numpy as np
from PIL import Image

CONFIG = 'C:\\Users\\Max\\Documents\\degeneracy\\detection_stuff\\yolov3.cfg'
WEIGHTS = 'C:\\Users\\Max\\Documents\\degeneracy\\detection_stuff\\yolov3.weights'
CLASSES = 'C:\\Users\\Max\\Documents\\degeneracy\\detection_stuff\\yolov3.txt'


def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def get_objects(pil_image: Image):
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    with open(CLASSES, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    net = cv2.dnn.readNet(WEIGHTS, CONFIG)

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    objects = {}

    for i in indices:
        class_name = classes[class_ids[i]]
        if class_name not in objects:
            objects[class_name] = 0
        objects[class_name] += 1

    return objects