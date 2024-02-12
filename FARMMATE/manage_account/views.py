from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms import FarmerLoginForm,FarmerRegistrationForm
from django.contrib.auth import  login, logout
from django.core.mail import send_mail,BadHeaderError
from django.contrib import messages
from .models import Farmer
from .custom_exceptions import USERNAMEEXISTS
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView ,LogoutView

class home(LoginRequiredMixin,TemplateView):
    template_name='dashboard/launch.html'
    



def generate_message(request,error):
    # Iterate through stored messages and discard them
        for message in messages.get_messages(request):
           pass
        messages.error(request,error)
    
# user registration view

class register(FormView):
    model=Farmer
    form_class=FarmerRegistrationForm
    enctype = 'multipart/form-data'
    template_name='manage_account/registration.html'
    redirect_authenticated_user=True
    success_url=reverse_lazy('userlogin')

    def form_valid(self, form: FarmerRegistrationForm) -> HttpResponse:
        password = form.cleaned_data.get('password1')
        confirm_password = form.cleaned_data.get('password2')

        if password != confirm_password:
            messages.error(self.request, "Passwords don't match.")
            return self.form_invalid(form)

        try:
            form.save()
            messages.success(self.request, "Account created successfully!")  # Display success message
        except USERNAMEEXISTS as e:  # Handle specific exceptions
            messages.error(self.request, f"Error: {e}")  # Display specific error message
        except Exception as e:  # Catch other exceptions
            messages.error(self.request, f"Unexpected error: {e}")

        return super().form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('userlogin')
        return super(register,self).get(*args,**kwargs)


def userLogin(request):
    try:
       
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            #calling the custom backend function
            user=authenticate(username=username, password=password)
            if user is not None:
                # Specify the backend explicitly when calling login() as we are using custom authentication backend 
                login(request, user)
                request.session['username'] =username

                messages.success(request, 'Login successful.')
                return redirect('home') 
            else:
                generate_message(request,"INVALID CREDENTIALS!!")
        else:
            pass
    except Exception as e:
        generate_message(request,e)

    return render(request, 'manage_account/login.html', {'form': FarmerLoginForm()})


class UserLogout(LogoutView) :
    next_page = reverse_lazy('userlogin')

