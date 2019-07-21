import cv2


def camera_init(number):
    cap = cv2.VideoCapture(0)
    return cap


def get_picture(cap):
    ret, frame = cap.read()
    return frame


def camera_release(cap):
    cap.release()
    cv2.destroyAllWindows()


def show_picture(frame):
    cv2.imshow("Test", frame)
    cv2.waitKey(1)