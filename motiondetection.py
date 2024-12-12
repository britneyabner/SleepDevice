import cv2
import imutils


def _subtract_images(image1, image2):
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(image1, image2)
    _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    return diff, thresh


def _detect_contours(binary_image) -> bool:
    dilated_image = cv2.dilate(binary_image, None, iterations=2)
    contours = cv2.findContours(dilated_image.copy(),
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for c in contours:
        if cv2.contourArea(c) > 700:
            return True
    return False


def detect_motion(image1, image2) -> bool:
    _, binary_image = _subtract_images(image1, image2)

    return _detect_contours(binary_image)
