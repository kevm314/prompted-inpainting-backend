import io
import os
import base64
import requests
import json
import numpy as np
from typing import Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image
from algorithms.prompted_figure_inpainting.src import preprocessor, pose_mask_generation
router = APIRouter()

@router.post("/prompted_inpainting_uploads")
async def root(
    prompt: str,
    base_image_file: UploadFile = File(...),
    mask_image_file: UploadFile = File(...),
):
    base_image_data = await base_image_file.read()
    mask_image_data = await mask_image_file.read()
    payload = {
        "prompt": prompt,
        "base_image": base64.b64encode(base_image_data).decode("utf-8"),
        "mask_image": base64.b64encode(mask_image_data).decode("utf-8"),
    }
    try:
        response = requests.post(
            os.environ["PROMPTED_INPAINTING_INFERENCE_URL"],
            json=payload
        )
    except Exception as e:
        return f'Error connecting to model inference endpoint: {e}'
    return response.json()

@router.post("/prompted_inpainting"
    # responses = {
    #     200: {
    #         "content": 
    #             {
    #                 "image/jpeg": {
    #             },

    #         },
    #         "content": 
    #             {
    #                 "application/json" : {
    #             }
    #         },
    #         "description": "Return the JSON item or an image."
    #     },
    # }
)
async def root(
    prompt: str,
    strength: float,
    base_image_file: UploadFile = File(...),
):
    base_image_data = await base_image_file.read()
    base_image_arr: np.ndarray = preprocessor.preprocessing(np.array(Image.open(BytesIO(base_image_data))))
    try:
        mask_image_arr, blob_type = pose_mask_generation.translate_prompt_to_body_blob(base_image_arr, prompt)
    except Exception as e:
        raise HTTPException(404, f'error interpreting prompt: {e}')
    if blob_type is None:
        res = json.dumps({
            "msg" : "Prompt could not be interpreted"
        })
        return Response(content=res, status_code=200, media_type="application/json")
    base_image: Image = Image.fromarray(base_image_arr)
    mask_image: Image = Image.fromarray(mask_image_arr)
    # encode images as base 64
    base_buffered = BytesIO()
    mask_buffered = BytesIO()
    base_image.save(base_buffered, format="JPEG")
    mask_image.save(mask_buffered, format="JPEG")
    base_image_str = base64.b64encode(base_buffered.getvalue())
    mask_image_str = base64.b64encode(mask_buffered.getvalue())
    payload = {
        "prompt": prompt,
        "strength": strength,
        "base_image": base_image_str.decode(),
        "mask_image": mask_image_str.decode(),
    }
    headers = {
        "Authorization": "Bearer ?",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            os.environ["PROMPTED_INPAINTING_INFERENCE_URL"],
            #headers=headers,
            json=payload
        )
    except Exception as e:
        return f'Error connecting to model inference endpoint: {e}'
    try:
        res: Any = response.json()
        content_str = res["image"]

        # post process to restore down sampled non-mask pixels
        buffered: BytesIO = preprocessor.postprocess(
            content_str=content_str,
            base_image_arr=base_image_arr,
            mask_image_arr=mask_image_arr
            )
    except Exception as e:
        raise HTTPException(404, f'error parsing model json response: {e}')
    return Response(content=buffered.getvalue(), media_type="image/jpeg")