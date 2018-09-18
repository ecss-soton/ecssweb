import os
from django.core.exceptions import ValidationError


def validate_photo_file_extension(file):
    ext = os.path.splitext(file.name)[1][1:]
    valid_extensions = ['jpg', 'jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('File extension \'{}\' is not allowed. Allowed extensions are: \'jpg, jpeg\'.'.format(ext))
