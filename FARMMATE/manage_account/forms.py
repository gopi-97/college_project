from django import forms
from .models import Farmer
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm
from .custom_exceptions import USERNAMEEXISTS


class FarmerRegistrationForm(UserCreationForm):

    profile_pic = forms.ImageField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''  # Remove password help text
        self.fields['password2'].help_text = ''  # Remove password help text

    def save(self, commit=True,*args, **kwargs):
        # Check if the username already exists
        username = self.cleaned_data['username']
        if Farmer.objects.filter(username=username).exists():
            raise USERNAMEEXISTS("Username already exists.")
        
        user = super(FarmerRegistrationForm, self).save(commit=False)
        user.profile_pic = self.cleaned_data['profile_pic']
        user.save()
        return super().save(commit=commit,*args, **kwargs)
    

    class Meta:
        model = Farmer
        fields = ['username','profile_pic','full_name','password1','password2','phone_number', 'email', 'company', 'address']
        attrs = {'class': 'register_form'}
        widgets={
            'username':forms.TextInput(attrs={'placeholder': 'Username', 'name' :'user_name', 'id': 'id_user_name', 'class': 'name'}),
            'profile_pic': forms.FileInput(attrs={'accept': 'image/*'}),
            'full_name':forms.TextInput(attrs={'placeholder': 'full name', 'name' :'full_name', 'id': 'id_full_name', 'class': 'name'}),
            'password1' : forms.PasswordInput( attrs={'placeholder': 'Password', 'name': 'password', 'id': 'password'}),
            'password2' : forms.PasswordInput( attrs={'placeholder': 'Confirm Password', 'name': 'password', 'id': 'confirm_password'}),
            'phone_number':forms.TextInput(attrs={'placeholder': 'Password', 'name': 'phone_number', 'value':'+91', 'id' : 'id_phone_number'}),
            'email':forms.EmailInput(attrs={'placeholder': 'enter email', 'id': 'id_email', 'placeholder': 'Email', 'name': 'email'}),
            'company':forms.TextInput(attrs={'placeholder': 'Company', 'name': 'company', 'id': 'id_company'}),
            'address':forms.Textarea(attrs={'placeholder': 'Address', 'name':'address', 'cols': 40, 'rows': 10, 'id': 'id_address'}),
        }
    message=forms.ValidationError("form cannot be validated,please try again")


class FarmerLoginForm(AuthenticationForm):
    class Meta:            
        model=Farmer
        fields=['username','password']
        attrs={'class': 'login-form'}
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username', 'id': 'username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter password', 'id': 'password'}),
        }

        