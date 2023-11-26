from django import forms
from .models import Client

class ClientRegi(forms.ModelForm):

    class Meta:
        model = Client  
        fields = ['first_name', 'last_name', 'password', 'usertype', 'phone_number', 'email', 'company', 'address']
        attrs = {'class': 'register_form'}

    message=forms.ValidationError("form cannot be validated,please try again")
   
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First name', 'name' :'first_name', 'id': 'id_first_name', 'class': 'name'})
    )


    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last name', 'name' :'last_name', 'id': 'id_first_name', 'class': 'name'})
    )


    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'name': 'password', 'id': 'id_password'})
    )

    USER_TYPES = [
        ('farmer', 'Farmer'),
        ('merchant', 'Merchant'),
    ]
    usertype = forms.ChoiceField(
        choices=USER_TYPES, 
        widget=forms.Select(attrs={'class': 'choice'})
    )


    phone_number=forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Password', 'name': 'phone_number', 'value':'+91', 'id' : 'id_phone_number'})
    )


    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'enter email', 'id': 'id_email', 'placeholder': 'Email', 'name': 'email'})
    )


    company=forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Company', 'name': 'company', 'id': 'id_company'})
    )
    address=forms.CharField(
        max_length=300,
        widget=forms.Textarea(attrs={'placeholder': 'Address', 'name':'address', 'cols': 40, 'rows': 10, 'id': 'id_address'})
    )


class ClientLogin(forms.ModelForm):
    class Meta:            
        model=Client
        fields=['userid','usertype','password']
        attrs={'class': 'login-form'}

    userid=forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'enter userid', 'name': 'userid', 'id': 'userid'})
    )
    password=forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': 'enter password', 'name': 'password', 'id': 'password'})
    )