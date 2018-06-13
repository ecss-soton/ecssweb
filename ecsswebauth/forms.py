from django import forms

class SamlRequestForm(forms.Form):
    next = forms.CharField(widget=forms.HiddenInput)
