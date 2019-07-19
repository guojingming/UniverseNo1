import cv2

from yolo_utils import yolo_util as yu


param = yu.init_params("../../")

cap = cv2.VideoCapture(0)

while 1:
    ret, img_ori = cap.read()
    img = yu.get_predict_result(img_ori, param)
    cv2.imshow("res", img)
    cv2.waitKey(1)