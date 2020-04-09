# coding=utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.core.validators import RegexValidator

from diary.models import Registration, Diary, Contact

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

phone_regex = RegexValidator(regex=r'^[0-9]+$', message="Enter a valid telephone number")
mobile_regex = RegexValidator(regex=r'^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$')



class UserLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )



class SignUpForm(UserCreationForm):
    telephone = forms.CharField(validators=[phone_regex], required=False)
    mobile_num = forms.CharField(validators=[mobile_regex], required=False)
    dob = forms.DateField(widget=forms.SelectDateWidget)


    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.request = request

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = Registration
        fields = ('username',
                  'name',
                  'gender',
                  'dob',
                  'photo',
                  'mobile_num',
                  'telephone',
                  'email', 'password1', 'password2', )





class UpdateProfile(forms.ModelForm):
    telephone = forms.CharField(validators=[phone_regex], required=False)
    mobile_num = forms.CharField(validators=[mobile_regex], required=False)
    dob = forms.DateField(widget=forms.SelectDateWidget)


    class Meta:
        model = Registration
        fields = ('username',
                  'name',
                  'gender',
                  'dob',
                  'photo',
                  'mobile_num',
                  'telephone',
                  'email')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(UpdateProfile, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user



class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = [
            "title",
            "content",
        ]

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'message']