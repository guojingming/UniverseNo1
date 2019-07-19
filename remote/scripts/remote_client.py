# coding: utf-8

from __future__ import division, print_function


import tensorflow as tf
import numpy as np
import argparse
import cv2
import time
import socket

from utils.misc_utils import parse_anchors, read_class_names
from utils.nms_utils import gpu_nms
from utils.plot_utils import get_color_table, plot_one_box

from model import yolov3

def recv_handler(cli_socket, count):
        buf = b''
        while count:
            newbuf = cli_socket.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf


parser = argparse.ArgumentParser(description="YOLO-V3 test single image test procedure.")
parser.add_argument("--input_image", type=str, default="./data/demo_data/dog.jpg",
                    help="The path of the input image.")
parser.add_argument("--anchor_path", type=str, default="./data/yolo_anchors.txt",
                    help="The path of the anchor txt file.")
parser.add_argument("--new_size", nargs='*', type=int, default=[416, 416],
                    help="Resize the input image with `new_size`, size format: [width, height]")
parser.add_argument("--class_name_path", type=str, default="./data/coco.names",
                    help="The path of the class names.")
parser.add_argument("--restore_path", type=str, default="./data/darknet_weights/yolov3.ckpt",
                    help="The path of the weights to restore.")
args = parser.parse_args()

args.anchors = parse_anchors(args.anchor_path)
args.classes = read_class_names(args.class_name_path)
args.num_class = len(args.classes)

color_table = get_color_table(args.num_class)

address = ("192.168.3.53", 6666)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)

with tf.Session() as sess:
    input_data = tf.placeholder(tf.float32, [1, args.new_size[1], args.new_size[0], 3], name='input_data')
    yolo_model = yolov3(args.num_class, args.anchors)
    with tf.variable_scope('yolov3'):
        pred_feature_maps = yolo_model.forward(input_data, False)
    pred_boxes, pred_confs, pred_probs = yolo_model.predict(pred_feature_maps)

    pred_scores = pred_confs * pred_probs

    boxes, scores, labels = gpu_nms(pred_boxes, pred_scores, args.num_class, max_boxes=200, score_thresh=0.3, nms_thresh=0.45)

    saver = tf.train.Saver()
    saver.restore(sess, args.restore_path)

    print("Waiting for connection.")
    cli_socket, cli_address = server_socket.accept()
    print("Connection building finished! Client's address is {0}".format(str(cli_address)))

    while 1:
        start = time.time()
        length = recv_handler(cli_socket, 16)
        string_data = recv_handler(cli_socket, int(length))
        data = np.frombuffer(string_data, np.uint8)
        img_ori = cv2.imdecode(data, cv2.IMREAD_COLOR)

        height_ori, width_ori = img_ori.shape[:2]
        img = cv2.resize(img_ori, tuple(args.new_size))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.asarray(img, np.float32)
        img = img[np.newaxis, :] / 255.

        boxes_, scores_, labels_ = sess.run([boxes, scores, labels], feed_dict={input_data: img})

        # rescale the coordinates to the original image
        boxes_[:, 0] *= (width_ori/float(args.new_size[0]))
        boxes_[:, 2] *= (width_ori/float(args.new_size[0]))
        boxes_[:, 1] *= (height_ori/float(args.new_size[1]))
        boxes_[:, 3] *= (height_ori/float(args.new_size[1]))


        end = time.time()
        seconds = end - start
        fps = 1/seconds


        # reconstruct result
        result = np.concatenate((boxes_[:, 0:4], np.zeros((len(boxes_), 1))), axis=1)
        result = result.astype(int)

        for i in range(len(boxes_)):
            result[i, -1] = labels_[i]

        result = result.reshape((-1))
        result_string = result.tostring()
        print("resultString: " + str(result))
        print("length: {0}".format(len(result_string)))
        cli_socket.send(str.encode(str(len(result_string)).ljust(16)))
        cli_socket.send(result_string)

            #plot_one_box(img_ori, [x0, y0, x1, y1], label=args.classes[labels_[i]], color=color_table[labels_[i]])

