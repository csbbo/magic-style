import os
import random
import sys
import logging
from concurrent import futures
import grpc
import settings
from core.test import convert_animal_style

from rpc import anime_style_pb2_grpc
from rpc.anime_style_pb2 import Image

logger = logging.getLogger('anime_style')


def rand_str(length=16):
    random_list = [random.choice("123456789abcdef") for i in range(length)]
    return "".join(random_list)


class Servicer(anime_style_pb2_grpc.StyleMigrateServicer):
    def ConvertAnimeStyle(self, request, context):
        upload_name = request.image_name
        upload_image_path = os.path.join(settings.UPLOAD_IMAGE_PATH, upload_name)

        image_name = rand_str()
        image_save_path = os.path.join(settings.GENERATE_IMAGE_PATH, image_name)

        convert_animal_style(image_path=upload_image_path, save_path=image_save_path)
        return Image(image_name=image_name)


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    anime_style_pb2_grpc.add_AnimeStyleServicer_to_server(Servicer(), server)
    server.add_insecure_port(settings.RPC_ADDR_PORT)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    sys.exit(server())
