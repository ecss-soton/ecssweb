from django import forms
from django.forms import ModelForm

from .models import Feedback, Response

class SubmitForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['category', 'message']

    def __init__(self, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({
            'rows': 3,
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

class RespondForm(ModelForm):
    class Meta:
        model = Response
        fields = ['message']

    def __init__(self, *args, **kwargs):
        super(RespondForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({
            'rows': 3,
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
