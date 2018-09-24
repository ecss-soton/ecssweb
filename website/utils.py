from PIL import Image
import io


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


def clean_image(image_file):
    if image_file:
        if image_file.size > 8*1024*1024:
            raise ValidationError("Photo file size too large. Supports file up to 8MB.")
        image = Image.open(image_file.file)
        image_format = image.format
        image = rotate_image(image)
        image_io = io.BytesIO()
        image.save(image_io, image_format)
        image_file.file = image_io
    return image_file
