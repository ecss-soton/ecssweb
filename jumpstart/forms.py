from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Helper, Group, ScavengerHunt

from website.utils import clean_image


class HelperEditProfileForm(ModelForm):
    class Meta:
        model = Helper
        fields = ['name', 'prefered_name', 'photo']

    def __init__(self, *args, **kwargs):
        super(HelperEditProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].disabled = True
        self.fields['photo'].widget.attrs.update({
            'accept': 'image/jpeg, image/png'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        return clean_image(photo)


class EditCityChallengeForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'charity_shop_challenge_photo']

    def __init__(self, *args, **kwargs):
        super(EditCityChallengeForm, self).__init__(*args, **kwargs)
        self.fields['charity_shop_challenge_photo'].widget.attrs.update({
            'accept': 'image/jpeg, image/png',
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    def clean_charity_shop_challenge_photo(self):
        photo = self.cleaned_data.get('charity_shop_challenge_photo', False)
        return clean_image(photo)


class EditScavengerHuntForm(ModelForm):
    class Meta:
        model = ScavengerHunt
        fields = ['photo']

    def __init__(self, *args, **kwargs):
        super(EditScavengerHuntForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({
            'accept': 'image/jpeg, image/png',
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                #'multiple': 'true',
            })

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        return clean_image(photo)


class ScoreMitreChallengeForm(ModelForm):
    class Meta:
        model = Group
        fields = ['mitre_challenge_score']

    def __init__(self, *args, **kwargs):
        super(ScoreMitreChallengeForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control mx-3',
            })


class ScoreCodingChallengeForm(ModelForm):
    class Meta:
        model = Group
        fields = ['coding_challenge_score']

    def __init__(self, *args, **kwargs):
        super(ScoreCodingChallengeForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control mx-3',
            })


class ScoreStagsQuizForm(ModelForm):
    class Meta:
        model = Group
        fields = ['stags_quiz_score']

    def __init__(self, *args, **kwargs):
        super(ScoreStagsQuizForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control mx-3',
            })


class ScoreGamesChallengeForm(ModelForm):
    class Meta:
        model = Group
        fields = ['games_challenge_score']

    def __init__(self, *args, **kwargs):
        super(ScoreGamesChallengeForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control mx-3',
            })


class ScoreSportsChallengeForm(ModelForm):
    class Meta:
        model = Group
        fields = ['sports_challenge_score']

    def __init__(self, *args, **kwargs):
        super(ScoreSportsChallengeForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control mx-3',
            })
