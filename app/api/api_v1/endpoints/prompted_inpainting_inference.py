import os
import base64
import requests
from fastapi import APIRouter, UploadFile, File, HTTPException
from io import BytesIO

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
            "http://127.0.0.1:8005/prompted_inpainting",#os.environ["PROMPTED_INPAINTING_INFERENCE_URL"],
            json=payload
        )
    except Exception as e:
        return f'Error connecting to model inference endpoint: {e}'
    return response.json()