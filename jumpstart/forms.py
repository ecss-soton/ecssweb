from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Helper, Fresher, Group, CharityShopChallengeSubmission, ScavengerHunt

from website.utils import clean_image


class HelperProfileEditForm(ModelForm):
    """Form for helpers to edit their profile."""

    class Meta:
        model = Helper
        fields = ['name', 'preferred_name', 'photo']


    def __init__(self, *args, **kwargs):
        super(HelperProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].disabled = True
        self.fields['photo'].widget.attrs.update({
            'accept': 'image/jpeg, image/png'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


    def clean_photo(self):
        photo = self.cleaned_data.get('photo', None)
        return clean_image(photo) if photo else photo


class FresherProfileEditForm(ModelForm):
    """Form for freshers to edit their profile."""

    class Meta:
        model = Fresher
        fields = ['name', 'preferred_name']


    def __init__(self, *args, **kwargs):
        super(FresherProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].disabled = True
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


class EditGroupNameForm(ModelForm):
    """Form for helpers to edit their group name."""

    class Meta:
        model = Group
        fields = ['name']


    def __init__(self, *args, **kwargs):
        super(EditGroupNameForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'required': 'required',
            })


    def clean_name(self):
        name = self.cleaned_data.get('name', None)
        if not name:
            raise ValidationError('Group name cannot be empty.')
        return name


class SubmitCharityShopChallengeForm(ModelForm):
    """Form for helpers to make charity shop challenge submissions."""

    class Meta:
        model = CharityShopChallengeSubmission
        fields = ['photo', 'description']


    def __init__(self, *args, **kwargs):
        super(SubmitCharityShopChallengeForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({
            'accept': 'image/jpeg, image/png',
        })
        self.fields['description'].widget.attrs.update({
            'rows': 3,
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    
    def clean_photo(self):
        photo = self.cleaned_data.get('photo', None)
        return clean_image(photo) if photo else photo


    def clean(self):
        super().clean()
        photo = self.cleaned_data.get('photo', None)
        description = self.cleaned_data.get('description', None)
        if not (photo or description):
            raise ValidationError('Photo and description cannot be both empty.')


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
            })

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        return clean_image(photo)


# class ScoreMitreChallengeForm(ModelForm):
#     class Meta:
#         model = Group
#         fields = ['mitre_challenge_score']

#     def __init__(self, *args, **kwargs):
#         super(ScoreMitreChallengeForm, self).__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control mx-3',
#             })


# class ScoreCodingChallengeForm(ModelForm):
#     class Meta:
#         model = Group
#         fields = ['coding_challenge_score']

#     def __init__(self, *args, **kwargs):
#         super(ScoreCodingChallengeForm, self).__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control mx-3',
#             })


# class ScoreStagsQuizForm(ModelForm):
#     class Meta:
#         model = Group
#         fields = ['stags_quiz_score']

#     def __init__(self, *args, **kwargs):
#         super(ScoreStagsQuizForm, self).__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control mx-3',
#             })


# class ScoreGamesChallengeForm(ModelForm):
#     class Meta:
#         model = Group
#         fields = ['games_challenge_score']

#     def __init__(self, *args, **kwargs):
#         super(ScoreGamesChallengeForm, self).__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control mx-3',
#             })


# class ScoreSportsChallengeForm(ModelForm):
#     class Meta:
#         model = Group
#         fields = ['sports_challenge_score']

#     def __init__(self, *args, **kwargs):
#         super(ScoreSportsChallengeForm, self).__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control mx-3',
#             })
