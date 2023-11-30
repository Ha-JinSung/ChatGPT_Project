from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm, AuthenticationForm
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class CustomUserCreationForm(UserCreationForm):
    nickname = forms.CharField(max_length=50)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('nickname',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
        user.profile.nickname = self.cleaned_data['nickname']
        if commit:
            user.profile.save()
        return user

class NicknameChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname']

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile

class PasswordChangeForm(AuthPasswordChangeForm):
    password_check = forms.CharField(max_length=32, widget=forms.PasswordInput, label='현재 비밀번호 확인')

    def clean_password_check(self):
        old_password = self.cleaned_data.get('이전 비밀번호')
        password_check = self.cleaned_data.get('비밀번호 체크')
        if password_check != old_password:
            raise forms.ValidationError('현재 비밀번호와 일치하지 않습니다.')
        return password_check

class UserDeleteForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserDeleteForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('비밀번호')
        user = get_user_model().objects.get(pk=self.request.user.pk)
        if not check_password(password, user.set_password):
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return password