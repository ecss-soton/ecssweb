from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Helper, Group

from website.utils import rotate_image

from PIL import Image
import io


class HelperEditProfileForm(ModelForm):
    class Meta:
        model = Helper
        fields = ['name', 'nickname', 'photo']

    def __init__(self, *args, **kwargs):
        super(HelperEditProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].disabled = True
        self.fields['photo'].widget.attrs.update({
            'accept': 'image/jpeg'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    # Check photo filesize
    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        if photo:
            if photo.size > 8*1024*1024:
                raise ValidationError("Photo file size too large. Supports file up to 8MB.")
            image = Image.open(photo.file)
            image_format = image.format
            image = rotate_image(image)
            image_io = io.BytesIO()
            image.save(image_io, image_format)
            photo.file = image_io
            return photo
        else:
            raise ValidationError("Couldn't read uploaded image.")


class EditCityChallengeForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(EditCityChallengeForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
