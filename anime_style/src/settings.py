import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VGG19_NPY_PATH = os.path.join(BASE_DIR, 'core/vgg19/vgg19.npy')
CHECKPOINT_DIR = os.path.join(BASE_DIR, 'core/checkpoint')

RPC_ADDR_PORT = '0.0.0.0:1600'

RESOURCES_DIR = os.path.abspath("/dev/resources")
IMAGES_PATH = os.path.join(RESOURCES_DIR, 'images')

UPLOAD_IMAGE_PATH = os.path.join(IMAGES_PATH, 'upload_image')
GENERATE_IMAGE_PATH = os.path.join(IMAGES_PATH, 'generate_image')


