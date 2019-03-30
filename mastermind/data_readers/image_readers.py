import numpy as np
import tensorflow as tf

from PIL import Image


def read_image_tensorflow(file_name, height=299, width=299, mean=0, std=255):
    file_reader = tf.read_file(file_name, name="file_reader")
    if file_name.endswith(".png"):
        image_reader = tf.image.decode_png(
            file_reader, channels=3, name="png_reader")
    elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(
            tf.image.decode_gif(file_reader, name="gif_reader"))
    elif file_name.endswith(".bmp"):
        image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
    else:
        image_reader = tf.image.decode_jpeg(
            file_reader, channels=3, name="jpeg_reader")
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [height, width])
    normalized = tf.divide(tf.subtract(resized, [mean]), [std])
    sess = tf.Session()
    return sess.run(normalized)


def read_image_pil(file_name, height=299, width=299, mean=0, std=255):
    image = Image.open(file_name).resize((width, height))
    image = np.array(image)
    image = np.expand_dims(image, 0)
    image = image - mean
    image = image / std
    return image
