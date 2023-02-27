import keras_cv
from tensorflow import keras
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import math
from PIL import Image
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument(
    "--prompt_1",
    type=str,
    nargs="?",
    default="a monkey on acid in interstellar space",
    help="the 1st prompt to render",
)

parser.add_argument(
    "--prompt_2",
    type=str,
    nargs="?",
    default="an octupus having a rave underwater",
    help="the 2nd prompt to render",
)

parser.add_argument("--index", type=int, default=0,
                    help="Index of the filename")
parser.add_argument(
    "--filename",
    type=str,
    nargs="?",
    default="output",
    help="filename without extension",
)

args = parser.parse_args()
print("use cmd-c to quit \n\n")
print(f"Begin image sequence {args.filename}{args.index}")
print(f"prompt 1 - {args.prompt_1}")
print(f"prompt 2 - {args.prompt_2}")
print(f"if you need to pause use ctrl-z, if you want to run in background after pause, type bg")
print("Good luck \n\n")

# Instantiate the Stable Diffusion model

model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)

# Funciton for creating gifs
def export_as_gif(filename, images, frames_per_second=10, rubber_band=False):
    if rubber_band:
        images += images[2:-1][::-1]
    images[0].save(
        filename,
        save_all=True,
        append_images=images[1:],
        duration=1000 // frames_per_second,
        loop=0,
    )

prompt_1 = ' '.join(f"{args.prompt_1},vivid colors, high detail, 4k, breathtaking, psychedelic art, trending on art station, unreal engine".split(' ')[:50])
prompt_2 = ' '.join(f"{args.prompt_2},vivid colors, high detail, 4k, breathtaking, psychedelic art, trending on art station, unreal engine".split(' ')[:50])

encoding_1 = tf.squeeze(model.encode_text(prompt_1))
encoding_2 = tf.squeeze(model.encode_text(prompt_2))

seed = len(args.prompt_1) + len(args.prompt_2) + random.randint(0, 666)
noise = tf.random.normal((512 // 8, 512 // 8, 4), seed=seed)

# Next
interpolation_steps = 15
batch_size = 1
batches = interpolation_steps // batch_size

interpolated_encodings = tf.linspace(
    encoding_1, encoding_2, interpolation_steps)
batched_encodings = tf.split(interpolated_encodings, batches)

images = []
for batch in range(batches):
    images += [
        Image.fromarray(img)
        for img in model.generate_image(
            batched_encodings[batch],
            batch_size=batch_size,
            num_steps=25,
            diffusion_noise=noise,
        )
    ]

export_as_gif(f"{args.filename}{args.index}.gif", images, rubber_band=False)
