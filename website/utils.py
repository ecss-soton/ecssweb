from PIL import Image, ExifTags


def is_committee(user):
    return user.groups.filter(name='committee').exists()


def rotate_image(image):
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
