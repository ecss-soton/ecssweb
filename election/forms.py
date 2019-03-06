from django import forms
from django.forms import ModelForm

from .models import Nomination

from website.utils import clean_image


class NominationForm(ModelForm):
    class Meta:
        model = Nomination
        fields = ['username', 'name', 'nickname', 'manifesto', 'photo']

    def __init__(self, *args, **kwargs):
        super(NominationForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['name'].disabled = True
        self.fields['photo'].widget.attrs.update({
            'accept': 'image/jpeg, image/png'
        })
        self.fields['manifesto'].widget.attrs.update({
            'rows': 3,
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        return clean_image(photo)
