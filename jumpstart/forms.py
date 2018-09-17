from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Helper

class HelperEditProfileForm(ModelForm):
    class Meta:
        model = Helper
        fields = ['name', 'nickname', 'photo']

    def __init__(self, *args, **kwargs):
        super(HelperEditProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].disabled = True
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    # Check photo filesize
    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        if photo:
            if photo._size > 4*1024*1024:
                raise ValidationError("Photo file size too large. Supports file up to 4MB.")
            return photo
        else:
            raise ValidationError("Couldn't read uploaded image.")
