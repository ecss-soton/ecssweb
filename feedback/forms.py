from django.forms import ModelForm

from .models import Feedback

class SubmitForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['category', 'message']

    def __init__(self, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields['message'].widget.attrs.update({
            'rows': 3,
        })