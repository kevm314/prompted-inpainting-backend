import sys
import json
import numpy as np
import cv2
from PIL import Image
import torch
from diffusers import StableDiffusionInpaintPipeline

class Model:
    def __init__(self, auth_token_path):
        try:
            with open(auth_token_path, "r") as f:
                auth_token = json.load(f)["SECRET"]
        except Exception as e:
            print(f'Huggingface token loading issue: {e}')
            sys.exit(1)
        inpainting_pipe = StableDiffusionInpaintPipeline.from_pretrained(
            "runwayml/stable-diffusion-inpainting",
            revision="fp16",
            torch_dtype=torch.float16,
            use_auth_token=auth_token
        )
        self.inpainting_pipe = inpainting_pipe.to("cuda")

    def infer(self, prompt: str, base_image: Image, mask_image: Image) -> Image:
        torch.cuda.empty_cache()
        #image and mask_image should be PIL images.
        #The mask structure is white for inpainting and black for keeping as is
        output_image = self.inpainting_pipe(prompt=prompt, image=base_image, mask_image=mask_image, num_inference_steps=100, strength=1).images[0]
        processed_output_img = np.asarray(output_image) * (np.asarray(mask_image) / 255) + np.asarray(base_image) * (1 - np.asarray(mask_image) / 255)
        return Image.fromarray(processed_output_img.astype(np.uint8))