import cv2
import numpy as np
import easyocr
import PIL.Image as pil_img

def Book_Image(Snap):

    pic = pil_img.open(Snap)
    img = np.array(pic).astype("uint8")
    picture = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image = cv2.rotate(picture, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image, detail=0)

    Words = [re for re in result]
    text = " ".join(Words)
    return text

