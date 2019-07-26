import cv2
import config as cfg


def camera_init(number):
    cap = cv2.VideoCapture(number)
    return cap


def get_picture(cap):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (cfg.window_width, cfg.window_height))
    result, imgencode = cv2.imencode('.jpg', frame)
    return result, imgencode


def camera_release(cap):
    cap.release()
    cv2.destroyAllWindows()


def show_picture(frame):
    cv2.imshow("Test", frame)
    cv2.waitKey(1)