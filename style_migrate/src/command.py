from core.backward import backward
from core.convert import conversion
from core.generateds import write_content_tfrecord
import argparse

parser = argparse.ArgumentParser()
args = parser.parse_args()

def original_to_style(image_path, label_weight, label_nums):
    return conversion(image_path, label_weight, label_nums)


def training_model():
    backward()


if __name__ == '__main__':
    write_content_tfrecord()
    backward()
    # label_weight = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # generate = original_to_style('./core/original_image/ts.jpg', label_weight, 20)
    # print(generate)
