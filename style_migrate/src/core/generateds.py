# -*- coding: UTF-8 -*-

import os
import tensorflow as tf
import numpy as np
from PIL import Image
import scipy.misc as misc
import settings

flags = tf.flags
flags.DEFINE_string('path_data', settings.DATA_PATH, 'tfRecord save path.')
flags.DEFINE_string('path_content', settings.COCO_DATA_PATH, 'Row style images path')
flags.DEFINE_string('record_dataset_name', 'coco_train.tfrecords', 'Data set tfrecord name')

flags.DEFINE_integer('img_h', 256, 'Train images\' height')
flags.DEFINE_integer('img_w', 256, 'Train images\' width')
flags.DEFINE_integer('img_c', 3, 'Train images\' channels num')
flags.DEFINE_integer('style_h', 512, 'Style images\' height')
flags.DEFINE_integer('style_w', 512, 'Style images\' width')

FLAGS = flags.FLAGS


def center_crop_img(img):
    """
    对图片按中心进行剪裁位正方形
    :param img: 原始图片
    :return:
    """
    width = img.size[0]
    height = img.size[1]
    offset = (width if width < height else height) / 2
    img = img.crop((
        width / 2 - offset,
        height / 2 - offset,
        width / 2 + offset,
        height / 2 + offset
    ))
    return img

def crop(img):
    h = img.shape[0]
    w = img.shape[1]

    if h < w:
        x = 0
        y = np.random.randint(0, w - h + 1)
        length = h
    elif h > w:
        x = np.random.randint(0, h - w + 1)
        y = 0
        length = w

    else:
        x = 0
        y = 0
        length = h
    return img[x:x + length, y:y + length, :]

def get_file_path_list():
    file_path_list = []
    # 读入coco原始数据集中文件路径集合
    for root, _, files in os.walk(FLAGS.path_content):
        for file in files:
            # 检查是否为图像文件
            if os.path.splitext(file)[1] not in ['.jpg', '.png', '.jpeg']:
                continue
            # 若是，则加入文件路径集合
            file_path = os.path.join(root, file)
            file_path_list.append(file_path)

    # 对路径集合进行打乱
    np.random.shuffle(file_path_list)
    return file_path_list

def write_content_tfrecord():
    if not os.path.exists(FLAGS.path_data):
        os.makedirs(FLAGS.path_data)
    writer = tf.python_io.TFRecordWriter(os.path.join(FLAGS.path_data, FLAGS.record_dataset_name))
    num_pic = 0
    
    for file_path in get_file_path_list():
        with Image.open(file_path) as img:
            img = center_crop_img(img)
            img = img.resize((FLAGS.img_w, FLAGS.img_h))
            img = img.convert('RGB')
            img_raw = img.tobytes()
            example = tf.train.Example(features=tf.train.Features(feature={
                'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
            }))
            num_pic += 1
            writer.write(example.SerializeToString())
            print('the number of picture:', num_pic)
    print('write tfrecord successful')


def read_content_tfrecord(path_tfrecord, image_size):
    filename_queue = tf.train.string_input_producer([path_tfrecord])
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example, features={
        'img_raw': tf.FixedLenFeature([], tf.string)
    })
    img = tf.decode_raw(features['img_raw'], tf.uint8)
    img.set_shape([image_size * image_size * 3])
    return img


def get_content_tfrecord(batch_size, path_tfrecord, image_size):
    """
    获取content_batch，用于训练
    :param batch_size:
    :param path_tfrecord: tfrecord存储路径
    :param image_size: 图片尺寸
    :return: content_batch op
    """
    img = read_content_tfrecord(path_tfrecord, image_size)
    img_batch = tf.train.shuffle_batch([img, ], batch_size=batch_size, num_threads=2, capacity=10, min_after_dequeue=1)
    return img_batch


def random_select_style(path, batch_size, shape, c_nums):
    filenames = os.listdir(path)
    # filenames = [i for i in filenames if i[-3:] == 'png']
    filenames = [i for i in filenames]
    rand_sample = np.random.randint(0, len(filenames))
    img = misc.imresize(crop(np.array(Image.open(os.path.join(path, filenames[rand_sample])))), [shape[0], shape[1]])
    batch = np.zeros([batch_size, shape[0], shape[1], shape[2]])
    y = np.zeros([1, c_nums])
    y[0, rand_sample] = 1
    for i in range(batch_size):
        batch[i, :, :, :] = img[:, :, :3]
    return batch, y

def main():
    write_content_tfrecord()


if __name__ == '__main__':
    main()
