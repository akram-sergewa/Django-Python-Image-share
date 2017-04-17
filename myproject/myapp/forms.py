# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from models import Drinker

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
    shared = forms.BooleanField(label='Shared with other users', required=False)
    fx = forms.BooleanField(label='FX image', required=False)
    description = forms.CharField(label='Description', required=False)

class EditForm(forms.Form):
    imageId = forms.CharField()
    shared = forms.BooleanField(label='Shared with other users', required=False)
    description = forms.CharField(label='Description', required=False)

class ChooseFXForm(forms.Form):
    imageId = forms.CharField()
    FX_URL = forms.CharField(label='Effects', required=False)
    
    
class RegistrationForm(ModelForm):
        username        = forms.CharField(label=(u'User Name'))
        email           = forms.EmailField(label=(u'Email Address'))
        password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
        password1       = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))

        class Meta:
                model = Drinker
                exclude = ('user',)

        def clean_username(self):
                username = self.cleaned_data['username']
                try:
                        User.objects.get(username=username)
                except User.DoesNotExist:
                        return username
                raise forms.ValidationError("That username is already taken, please select another.")

        def clean(self):
                if self.cleaned_data['password'] != self.cleaned_data['password1']:
                        raise forms.ValidationError("The passwords did not match.  Please try again.")
                return self.cleaned_data

class LoginForm(forms.Form):
        username        = forms.CharField(label=(u'User Name'))
        password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
