from django import forms

from django.contrib.auth.models import User


class MyUserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Password Confirm", required=True, widget=forms.PasswordInput,  strip=False)

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
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']