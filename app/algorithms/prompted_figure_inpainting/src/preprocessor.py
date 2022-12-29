import cv2
import base64
import numpy as np

from io import BytesIO
from PIL import Image

def process_input(image_path: str) -> np.ndarray:
    primary_image_arr = cv2.imread(image_path)
    primary_image_arr = cv2.cvtColor(primary_image_arr, cv2.COLOR_BGR2RGB)
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

def postprocess(content_str: str, base_image_arr: np.ndarray, mask_image_arr: np.ndarray) -> BytesIO:
    output_image = Image.open(BytesIO(base64.b64decode(content_str)))
    processed_output_img = restore_mask(output_image, base_image_arr, mask_image_arr)
    # encode image as base 64
    buffered = BytesIO()
    processed_output_img.save(buffered, format="JPEG")
    return buffered

def restore_mask(
        output_image: Image,
        base_image_arr: np.ndarray,
        mask_image_arr: np.ndarray
    ) -> Image:
    processed_output_img = np.asarray(output_image) * (mask_image_arr / 255) + base_image_arr * (1 - mask_image_arr / 255)
    processed_output_img = Image.fromarray(processed_output_img.astype(np.uint8))
    return processed_output_img