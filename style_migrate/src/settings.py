import os


RPC_ADDR_PORT = '0.0.0.0:1600'

# RESOURCES_DIR = os.path.abspath("./core")
RESOURCES_DIR = os.path.abspath("/dev/resources")

MODEL_PATH = os.path.join(RESOURCES_DIR, "model")

IMAGES_PATH = os.path.join(RESOURCES_DIR, 'images')
UPLOAD_IMAGE_PATH = os.path.join(IMAGES_PATH, 'upload')
GENERATE_IMAGE_PATH = os.path.join(IMAGES_PATH, 'generate_image')
STYLE_IMAGE_PATH = os.path.join(IMAGES_PATH, 'style_image')

VGGNET_PATH = os.path.join(RESOURCES_DIR, 'vggnet')
DATA_PATH = os.path.join(RESOURCES_DIR, 'data')
COCO_DATA_PATH = os.path.join(RESOURCES_DIR, 'MSCOCO')


class TrainingModeTypeEnum:
    start = 'start'
    stop = 'stop'
    status = 'status'
