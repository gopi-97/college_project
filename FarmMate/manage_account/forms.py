from django import forms
from .models import Client

class ClientRegi(forms.ModelForm):
      # Define a BooleanField for the usertype
    message=forms.ValidationError("form cannot be validated,please try again")
    # usertype = forms.ChoiceField(
    #     widget=forms.RadioSelect(choices=[('Farmer', 'Farmer'), ('Merchant', 'Merchant')]),
    #     required=True
    # )
    class Meta:
        model=Client
        fields=['first_name','last_name','usertype','password','phone_number','email','company','address']

class ClientLogin(forms.ModelForm):
    class Meta:            
        model=Client
        fields=['userid','usertype','password']