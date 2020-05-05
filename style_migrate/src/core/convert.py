import tensorflow as tf
import numpy as np
from PIL import Image
from core.forward import forward
import os
import settings
from utils.shortcuts import rand_str, read_image


def conversion(image_path, label_weight, label_nums):
    content = tf.placeholder(tf.float32, [1, None, None, 3])
    weight = tf.placeholder(tf.float32, [1, label_nums])
    target = forward(content, weight)

    feed_content = read_image(image_path)
    feed_content = feed_content[np.newaxis, :, :, :]

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        ckpt = tf.train.get_checkpoint_state(settings.MODEL_PATH)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
        image = sess.run(target, feed_dict={content: feed_content, weight: label_weight})

    img_name = rand_str()
    file_name = os.path.join(settings.GENERATE_IMAGE_PATH, img_name+'.png')
    Image.fromarray(np.uint8(image[0, :, :, :])).save(file_name)
    return img_name+'.png'


# if __name__ == '__main__':
#     conversion()
