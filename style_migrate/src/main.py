import subprocess
import sys
import logging
import time
from concurrent import futures
import grpc
import settings
import numpy as np
import os
from command import original_to_style

from rpc import style_migrate_pb2_grpc
from rpc.style_migrate_pb2 import Response, GenerateImage

logger = logging.getLogger('style_migrate')


class Servicer(style_migrate_pb2_grpc.StyleMigrateServicer):
    child = -9

    def ConvertImage(self, request, context):
        origin_image = request.origin_image
        label_weight = request.label_weight
        style_files = os.listdir(settings.STYLE_IMAGE_PATH)
        # style_files = sorted(style_files)
        label_nums = len(style_files)
        weight = np.zeros([1, label_nums])
        for lw in label_weight:
            file_position = style_files.index(lw.image_name)
            weight[0, file_position] = round(lw.weight, 1)

        start_time = time.time()
        logger.info('convert image start')
        print(weight)
        generate_image = original_to_style(image_path=os.path.join(settings.UPLOAD_IMAGE_PATH, origin_image),
                                           label_weight=weight, label_nums=label_nums)
        print(generate_image)
        spend_time = time.time() - start_time
        logger.info(f'convert finish spend {spend_time}')

        response = Response(status=True, message='succeed')
        return GenerateImage(response=response, generate_image=generate_image)

    def TrainingModel(self, request, context):
        command = request.command
        message = 'success'
        if command == settings.TrainingModeTypeEnum.start:
            if Servicer.child == -9:
                Servicer.child = subprocess.Popen('python3 command.py', shell=True)
                message = 'start succeed!'
            else:
                return Response(status=False, message='The model is being trained')
        if command == settings.TrainingModeTypeEnum.stop:
            if Servicer.child != -9:
                Servicer.child.kill()
                Servicer.child = -9
                message = 'stop succeed!'
            else:
                return Response(status=False, message='The model has not yet been trained')
        if command == settings.TrainingModeTypeEnum.status:
            if Servicer.child == -9:
                message = 'stopping'
            else:
                message = 'training'
        return Response(status=True, message=message)


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    style_migrate_pb2_grpc.add_StyleMigrateServicer_to_server(Servicer(), server)
    server.add_insecure_port(settings.RPC_ADDR_PORT)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    sys.exit(server())
