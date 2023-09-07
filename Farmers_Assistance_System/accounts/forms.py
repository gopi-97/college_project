from django import forms
from.models import Users

class Userforms(forms.ModelForm):
    class Meta:
        model=Users
        fields=['username','userid','password','usertype']