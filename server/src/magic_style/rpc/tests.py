import logging

import grpc

from style_migrate.style_migrate_pb2_grpc import StyleMigrateStub
from style_migrate.style_migrate_pb2 import Action, ImageLabelWeight, LabelWeight

logger = logging.getLogger(__name__)


def training_mode():
    with grpc.insecure_channel('127.0.0.1:1600') as channel:
        stub = StyleMigrateStub(channel)
        # action = Action(command='start')
        action = Action(command='status')
        # action = Action(command='stop')
        resp = stub.TrainingModel(action)
        print(resp)
        return resp


def convert_image():
    with grpc.insecure_channel('127.0.0.1:1600') as channel:
        stub = StyleMigrateStub(channel)
        label_weight = [LabelWeight(image_name='2.png', weight=0.3), LabelWeight(image_name='3.png', weight=0.7)]
        image_label_weight = ImageLabelWeight(origin_image='ts.jpg', label_weight=label_weight)
        resp = stub.ConvertImage(image_label_weight)
        print(resp)
        print(resp.response.status)
        print(resp.generate_image)
        return resp


if __name__ == '__main__':
    # training_mode()
    convert_image()
