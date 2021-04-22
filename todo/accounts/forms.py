from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User

from accounts.models import Profile


class MyUserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Password Confirm", required=True, widget=forms.PasswordInput, strip=False)

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        last_name = cleaned_data.get('last_name')
        first_name = cleaned_data.get('first_name')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        if len(last_name) == 0 and len(first_name) == 0:
            raise forms.ValidationError('Заполните хотя б одну из полей first или last name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user','avatar', 'about_me', 'links']
        widgets = {
            'about_me': forms.Textarea(attrs={'cols': 50, 'rows': 10})
        }


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class PasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(required=True,label='Старый пароль')
    new_password = forms.CharField(required=True,label='Новый пароль')
    password_confirm = forms.CharField(required=True,label='Подтверждение пароля')

    class Meta:
        model = get_user_model()
        fields = ['new_password', 'password_confirm', 'old_password']

    def clean_password_confirm(self):
        new_password = self.cleaned_data.get("new_password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if new_password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return new_password

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data.get('new_password'))
        if commit:
            user.save()
        return user