from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(required=False, label='Username')
    email = forms.CharField(required=True, label='Email')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)
    next = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm password', strip=False, required=True,
                                       widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('role', 'username', 'email', 'phone', 'password', 'password_confirm', 'profile_photo')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match!')
        email = cleaned_data.get('email')
        if not email:
            raise ValidationError({'email': 'Email is required field'})
        phone = cleaned_data.get('phone')
        if not phone:
            raise ValidationError({'phone': 'Phone is required field'})

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data.get('password'))
    #     user_group = Group.objects.get(name='user')
    #     user.groups.add(user_group)
    #     if commit:
    #         user.save()
    #     return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'phone', 'profile_photo')
