from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError


def is_committee(user):
    return user.groups.filter(name='committee').exists()


def rotate_image(image):
    """ Rotate an image according to it's exif info. """

    try:
        orientation_tag = 274 # 0x0112
        exif=dict(image._getexif().items())
        if exif[orientation_tag] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation_tag] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation_tag] == 8:
            image = image.rotate(90, expand=True)
    except(AttributeError, KeyError, IndexError):
        pass
    return image


def reconstruct_image_file(image, filename, image_format):
    """Reconstruct Django File from PIL image.
       Also strip EXIF data.
    """
    image_io = io.BytesIO()
    image.save(image_io, image_format)
    image_file = InMemoryUploadedFile(image_io, None, filename, image_format, None, None, None)
    return image_file


def validate_file_size(f, size_limit):
    if f.size > size_limit*1024*1024:
        raise ValidationError('File size too large. File size limited to {}MB.'.format(size_limit))


def clean_image(image_file, size_limit=8):
    """Validate file size, rotate image and strip EXIF data."""

    if size_limit:
        validate_file_size(image_file, size_limit)
    image = Image.open(image_file)
    filename = image_file.name
    image_format = image.format
    image = rotate_image(image)
    image_file = reconstruct_image_file(image, filename, image_format)
    return image_file
