from . import Choices


class ImageTypeEnum(Choices):
    original_image = 'original_image'
    style_image = 'style_image'
    style_image_ready = 'style_image_ready'
    generate_image = 'generate_image'
    other = 'other'
