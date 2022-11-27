from typing import Tuple
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import numpy as np
import cv2
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose

def torso_buffer(coordinates):
    return int(0.33 * np.linalg.norm(coordinates[1] - coordinates[0]))

def arm_buffer(coordinates):
    return int(0.2 * np.linalg.norm(coordinates[1] - coordinates[0]))

def bottom_buffer(coordinates):
    return int(0.2 * np.linalg.norm(coordinates[1] - coordinates[0]))

def feet_buffer(coordinates):
    return int(0.1 * np.linalg.norm(coordinates[1] - coordinates[0]))

object_blob_mapping = {
    # bottom_half
    "pants": "bottom_half",
    "trousers": "bottom_half",
    "jeans": "bottom_half",
    "skirt": "bottom_half",
    "leggings": "bottom_half",
    "sweatpants": "bottom_half",
    # top_half
    "shirt": "top_half",
    "jacket": "top_half",
    "top": "top_half",
    "t-shirt": "top_half",
    "tshirt": "top_half",
    "sweater": "top_half",
    "jumper": "top_half",
    "cardigan": "top_half",
    "tie": "top_half",
    # right_arm
    "sleeve": "right_arm",
    # feet
    "shoes": "feet",
    "shoe": "feet",
    "heels": "feet",
    "boots": "feet",
    "sneakers": "feet",
    "slippers": "feet",
    "thongs": "feet",
    "flops": "feet",
    "crocs": "feet",
    "ugg": "feet",
}

body_blobs = {
    "torso": {
        "coords": [12, 11, 23, 24, 12],
        "buffer": torso_buffer,
        "cap_style": 1
    },
    "right_arm": {
        "coords": [12, 14, 16],
        "buffer": arm_buffer,
        "cap_style": 1
    },
    "left_arm": {
        "coords": [11, 13, 15],
        "buffer": arm_buffer,
        "cap_style": 1
    },
    "top_half": {
        "coords": [20, 14, 12, 24, 23, 11, 12, 11, 13, 19],
        "buffer": arm_buffer,
        "cap_style": 1
    },
    "bottom_half": {
        "coords": [28, 26, 24, 23, 25, 27],
        "buffer": bottom_buffer,
        "cap_style": 3
    },
    "bottom_half_shorts": {
        "coords": [26, 24, 23, 25],
        "buffer": bottom_buffer,
        "cap_style": 3
    },
    "feet": {
        "coords": [32, 30, 28, 32],
        "buffer": feet_buffer,
        "cap_style": 1
    }
}

def generate_outline(pose_landmarks, keyword_blob) -> np.ndarray:
    blob_selection = body_blobs[keyword_blob]
    coordinates = []
    for index in blob_selection["coords"]:
        coordinates.append(pose_landmarks[index])
    blob = LineString(coordinates=coordinates)
    buffer_mag = blob_selection["buffer"](coordinates)
    blob = blob.buffer(buffer_mag, cap_style=blob_selection["cap_style"])
    return np.array(blob.exterior.coords).astype(np.int32)

def generate_landmarks(input_frame: np.ndarray):
    """ Generate landmarks for the provided input frame. """
    input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
    # Initialize fresh pose tracker and run it.
    with mp_pose.Pose() as pose_tracker:
        result = pose_tracker.process(image=input_frame)
        pose_landmarks = result.pose_landmarks

    pose_landmarks = [[lmk.x, lmk.y, lmk.z] for lmk in pose_landmarks.landmark]

    # Map pose landmarks from [0, 1] range to absolute coordinates to get
    # correct aspect ratio.
    frame_height, frame_width = input_frame.shape[:2]
    pose_landmarks *= np.array([frame_width, frame_height, frame_width])

    # Draw pose landmarks on the image.
    mp_drawing.draw_landmarks(
        input_frame,
        result.pose_landmarks,
        mp_pose.POSE_CONNECTIONS)
    return pose_landmarks, result

def generate_mask(src_img, blob_type) -> np.ndarray:
    pose_landmarks, result = generate_landmarks(src_img)
    mask = np.zeros(src_img.shape)
    blob_arr = generate_outline(pose_landmarks, blob_type)
    cv2.fillPoly(mask, pts=[blob_arr], color=(255, 255, 255))
    return mask.astype(np.uint8)

def translate_prompt_to_body_blob(input_frame: np.ndarray, prompt: str) -> Tuple[np.ndarray, str]:
    """ 
        Generate a crude mask for the on-body object contained in the prompt.
        The first prompt found in the mapping table is used to generate the mask.
    """
    blob_type = None
    for word in prompt.split(" "):
        if word in object_blob_mapping.keys():
            blob_type = object_blob_mapping[word]
            break
    mask = generate_mask(input_frame, blob_type)
    return mask, blob_type