# -*- coding: UTF-8 -*-

from core.forward import vggnet, forward, get_content_loss, get_style_loss
import tensorflow as tf

from core.generateds import get_content_tfrecord
from core.generateds import random_select_style
import numpy as np
import argparse
import time
import os
import settings

# 初始化各种参数
parser = argparse.ArgumentParser()
# 输入图像尺寸
parser.add_argument("--IMG_H", type=int, default=256)
parser.add_argument("--IMG_W", type=int, default=256)
parser.add_argument("--IMG_C", type=int, default=3)
# 风格图像尺寸
parser.add_argument("--STYLE_H", type=int, default=512)
parser.add_argument("--STYLE_W", type=int, default=512)
# 风格图像张数
parser.add_argument("--LABELS_NUMS", type=int, default=20)
# Batch大小，默认为2
parser.add_argument("--BATCH_SIZE", type=int, default=2)
# 学习率
parser.add_argument("--LEARNING_RATE", type=float, default=0.001)
# 内容权重和风格权重
parser.add_argument("--CONTENT_WEIGHT", type=float, default=1.0)
parser.add_argument("--STYLE_WEIGHT", type=float, default=10.0)
# 风格图像路径
parser.add_argument("--PATH_STYLE", type=str, default=settings.STYLE_IMAGE_PATH)
# 生成模型路径
parser.add_argument("--PATH_MODEL", type=str, default=settings.MODEL_PATH)
# VGG16路径
parser.add_argument("--PATH_VGG16", type=str, default=settings.VGGNET_PATH)
# 数据集路径
parser.add_argument("--PATH_DATA", type=str, default=settings.DATA_PATH)
# 数据集名称
parser.add_argument("--DATASET_NAME", type=str, default="coco_train.tfrecords")
# 训练轮数
parser.add_argument("--steps", type=int, default=50000)
args = parser.parse_args()


def backward(img_h=args.IMG_H, img_w=args.IMG_W, img_c=args.IMG_C, style_h=args.STYLE_H, style_w=args.STYLE_W,
             c_nums=args.LABELS_NUMS, batch_size=args.BATCH_SIZE, learning_rate=args.LEARNING_RATE,
             content_weight=args.CONTENT_WEIGHT, style_weight=args.STYLE_WEIGHT, path_style=args.PATH_STYLE,
             model_path=args.PATH_MODEL, vgg_path=args.PATH_VGG16, path_data=args.PATH_DATA,
             dataset_name=args.DATASET_NAME):
    content = tf.placeholder(tf.float32, [batch_size, img_h, img_w, img_c])
    style = tf.placeholder(tf.float32, [batch_size, style_h, style_w, img_c])
    weight = tf.placeholder(tf.float32, [1, c_nums])
    target = forward(content, weight)
    vgg_target = vggnet(target, vgg_path)
    vgg_content = vggnet(content, vgg_path)
    vgg_style = vggnet(style, vgg_path)
    content_loss = get_content_loss(vgg_content, vgg_target)

    style_loss = get_style_loss(vgg_style, vgg_target)
    loss = content_loss * content_weight + style_loss * style_weight

    global_step = tf.Variable(0, trainable=False)

    opt = tf.train.AdamOptimizer(learning_rate).minimize(loss, global_step=global_step)

    content_batch = get_content_tfrecord(batch_size, os.path.join(path_data, dataset_name), img_h)

    saver = tf.train.Saver()
    time_start = time.time()

    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)

        ckpt = tf.train.get_checkpoint_state(model_path)

        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            print('Restore Model Successfully')
        else:
            print('No Checkpoint Found')

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        for itr in range(args.steps):
            time_step_start = time.time()
            batch_content = sess.run(content_batch)
            batch_content = np.reshape(batch_content, [batch_size, img_w, img_h, img_c])
            batch_style, y_labels = random_select_style(path_style, batch_size, [style_h, style_w, img_c], c_nums)
            sess.run(opt, feed_dict={content: batch_content, style: batch_style, weight: y_labels})
            step = sess.run(global_step)

            time_step_stop = time.time()
            a = 200
            if itr % a == 0:
                saver.save(sess, os.path.join(model_path, 'model'), global_step=global_step)
                print('Iteration: %d, Save Model Successfully, single step time = %.2fs, total time = %.2fs' % (
                    step, time_step_stop - time_step_start, time_step_stop - time_start))

        coord.request_stop()
        coord.join(threads)
#
#
# def main():
#     backward()
#
# if __name__ == '__main__':
#     main()
