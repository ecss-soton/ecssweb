from django.forms import ModelForm

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