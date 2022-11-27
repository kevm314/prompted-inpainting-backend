import cv2
import numpy as np

def process_input(image_path: str) -> np.ndarray:
    primary_image_arr = cv2.imread(image_path)
    return primary_image_arr

def preprocessing(primary_image_arr: np.ndarray) -> np.ndarray:
    return resize_with_border(primary_image_arr)

def resize_with_border(primary_image_arr: np.ndarray, desired_size=512) -> np.ndarray:
    # old_size is in (height, width) format
    old_size = primary_image_arr.shape[:2]

    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    # new_size should be in (width, height) format
    im = cv2.resize(primary_image_arr, (new_size[1], new_size[0]))

    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)

    color = [0, 0, 0]
    primary_image_arr = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return primary_image_arr