from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Client
import time
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home/home.html')


def registrationForm(request):
    if request.method == 'POST':
        form_data = request.POST.dict() 
        user = Client(
            full_name=form_data['full_name'],
            phone_number=form_data['phone_number'],
            email=form_data['email'],
            company=form_data['company'],
            address=form_data['address'],
        )
        user.set_password(form_data['password'])
        user.save()
        messages.success(request, 'Registration successful. You can now login.')
        return redirect('login')

    return render(request, 'Accounts/registration.html')


def loginForm(request):
    if request.method == 'POST':
        userid = request.POST['userid']
        password = request.POST['password']
        user = authenticate(request, username=userid, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            time.sleep(1)
            return redirect('home')  
        else:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'Accounts/login.html')
    else:
        return render(request, 'Accounts/login.html')



def logoutUser(request):
    request.session.flush()
    logout(request)
    return redirect('login')