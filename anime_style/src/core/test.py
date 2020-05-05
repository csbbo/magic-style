import argparse
from utils import *
import os
import time
import numpy as np
from net import generator
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT_DIR = os.path.join(BASE_DIR, 'checkpoint/AnimeGAN_Hayao_lsgan_300_300_1_3_10')
def parse_args():
    desc = "Tensorflow implementation of AnimeGAN"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--checkpoint_dir', type=str, default='checkpoint/'+'AnimeGAN_Shinkai_lsgan_300_300_1_3_10',
                        help='Directory name to save the checkpoints')
    parser.add_argument('--test_image', type=str, default='dataset/test/real',
                        help='Directory name of test photos')
    parser.add_argument('--style_name', type=str, default='S',
                        help='what style you want to get')
    parser.add_argument('--save_path', type=str, default='./save.jpg',
                        help='file path')

    """checking arguments"""

    return parser.parse_args()


def stats_graph(graph):
    flops = tf.profiler.profile(graph, options=tf.profiler.ProfileOptionBuilder.float_operation())
    # params = tf.profiler.profile(graph, options=tf.profiler.ProfileOptionBuilder.trainable_variables_parameter())
    print('FLOPs: {}'.format(flops.total_float_ops))


def convert_animal_style(image_path, save_path, img_size=[256,256], checkpoint_dir=CHECKPOINT_DIR):
    # tf.reset_default_graph()
    # test_real = tf.placeholder(tf.float32, [1, 256, 256, 3], name='test')
    test_real = tf.placeholder(tf.float32, [1, None, None, 3], name='test')

    with tf.variable_scope("generator", reuse=False):
        test_generated = generator.G_net(test_real).fake
    saver = tf.train.Saver()

    gpu_options = tf.GPUOptions(allow_growth=True)
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, gpu_options=gpu_options)) as sess:
        # tf.global_variables_initializer().run()
        # load model
        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)  # checkpoint file information
        if ckpt and ckpt.model_checkpoint_path:
            ckpt_name = os.path.basename(ckpt.model_checkpoint_path)  # first line
            saver.restore(sess, os.path.join(checkpoint_dir, ckpt_name))
            print(" [*] Success to read {}".format(ckpt_name))
        else:
            print(" [*] Failed to find a checkpoint")
            return

        stats_graph(tf.get_default_graph())

        begin = time.time()
        sample_image = np.asarray(load_test_data(image_path, img_size))
        fake_img = sess.run(test_generated, feed_dict = {test_real : sample_image})
        save_images(fake_img, save_path)
        end = time.time()
        print(f'test-time: {end-begin} s')

if __name__ == '__main__':
    arg = parse_args()
    convert_animal_style(arg.test_image, arg.save_path)
