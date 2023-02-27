import time
import keras_cv
from tensorflow import keras
import matplotlib.pyplot as plt
import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument(
    "--p",
    type=str,
    default="Goldfish in a bowl",
    help="Prompt for Stable diffusion"
)
parser.add_argument(
    "--output",
    type=str,
    nargs="?",
    default="output.png",
    help="where to save the output image",
)
parser.add_argument(
    "--steps", type=int, default=50, help="number of ddim sampling steps"
)
args = parser.parse_args()
print(f"rendering - {args.p}")


model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)

prompt = f"{args.p}"
images = model.text_to_image(
    prompt, batch_size=1,num_steps=args.steps)

Image.fromarray(images[0]).save(args.output)

# def plot_images(images):
#     plt.figure(figsize=(20, 20))
#     for i in range(len(images)):
#         ax = plt.subplot(1, len(images), i + 1)
#         plt.imshow(images[i])
#         plt.axis("off")


# plot_images(images)
# plt.show()
