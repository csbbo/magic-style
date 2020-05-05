import logging

import grpc
from django.conf import settings

from rpc.style_migrate.style_migrate_pb2_grpc import StyleMigrateStub
from rpc.style_migrate.style_migrate_pb2 import Action, LabelWeight, ImageLabelWeight
from rpc.anime_style.anime_style_pb2_grpc import AnimeStyleStub
from rpc.anime_style.anime_style_pb2 import Image
from utils.constants.rpc import TrainingModeTypeEnum

logger = logging.getLogger(__name__)


def training_mode(command=TrainingModeTypeEnum.status):
    with grpc.insecure_channel(settings.SM_RPC_HOST_PORT) as channel:
        stub = StyleMigrateStub(channel)
        action = Action(command=command)
        response = stub.TrainingModel(action)
        return response


def convert_image(origin_image, weight):
    with grpc.insecure_channel(settings.SM_RPC_HOST_PORT) as channel:
        stub = StyleMigrateStub(channel)
        label_weight = []
        for k, v in weight.items():
            label_weight.append(LabelWeight(image_name=k, weight=v))
        image_label_weight = ImageLabelWeight(origin_image=origin_image, label_weight=label_weight)
        resp = stub.ConvertImage(image_label_weight)
        return resp.generate_image


def convert_anime_style(image_name):
    with grpc.insecure_channel(settings.AS_RPC_HOST_PORT) as channel:
        stub = AnimeStyleStub(channel)
        image = Image(image_name=image_name)
        resp = stub.ConvertAnimeStyle(image)
        return resp.image_name
