import matplotlib.pyplot as plt
from PIL import Image
import cv2

import model
import preprocessor
import pose_mask_generation

def run():
    # Give me a ...
    prompt = "a pink hawaiian shirt"

    IMAGE_PATH = "../text2img/sample_images/side_poser.png"
    
    print("Loading model")
    diffusion_model = model.Model("../auth.json") 
    
    print("load image + preprocess")
    primary_image_arr = preprocessor.process_input(IMAGE_PATH)
    #plt.imshow(cv2.cvtColor(primary_image_arr, cv2.COLOR_BGR2RGB))
    #plt.show()

    print("generating pose mask")
    mask_image_arr, blob_type = pose_mask_generation.translate_prompt_to_body_blob(primary_image_arr, prompt)
    print("Blob type identified:", blob_type)
    #plt.imshow(cv2.cvtColor(primary_image_arr, cv2.COLOR_BGR2RGB))
    #plt.imshow(mask_image_arr, cmap='jet', alpha=0.5)
    #plt.show()

    print("generate inpainting result")
    base_input_image = Image.fromarray(cv2.cvtColor(primary_image_arr, cv2.COLOR_BGR2RGB))
    mask_input_image = Image.fromarray(cv2.cvtColor(mask_image_arr, cv2.COLOR_BGR2RGB))
    output_image: Image = diffusion_model.infer(prompt=prompt, base_image=base_input_image, mask_image=mask_input_image)

    print("save result to disk")
    output_image.save("./inpainted_sample.png")    







if __name__ == "__main__":
    run()