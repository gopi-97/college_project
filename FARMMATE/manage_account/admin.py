from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import FarmerRegistrationForm, FarmerLoginForm
from .models import Farmer

class CustomUserAdmin(UserAdmin):
    add_form = FarmerRegistrationForm
    form = FarmerLoginForm
    model = Farmer
    list_display = [ "username",'password']

admin.site.register(Farmer)