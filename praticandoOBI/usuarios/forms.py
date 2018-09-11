from django import forms
from django.contrib.auth.models import User
from .models import Profile
from provasobi.models import ProvaPerson

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('localizacao', 'data_nascimento',)

class ProvaForm(forms.ModelForm):
    class Meta:
        model = ProvaPerson
        fields = ('titulo', 'ano', 'observacoes',)