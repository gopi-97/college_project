from django.shortcuts import render, redirect
from .forms import ClientRegi as cr, ClientLogin as cl
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail,BadHeaderError
from django.contrib import messages
from .models import Client
import random
import string

from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')


def generate_userid():
    chars = string.ascii_letters + string.digits
    id = "".join(random.choice(chars) for _ in range(10)) #generator function
    return id

# user registration form
def registrationForm(request):
    if request.method == 'POST':
        form = cr(request.POST)
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                
                # this line creates a list of all the userids in the client model
                existing_ids = [user.userid for user in Client.objects.all()]
        
                unique_id = generate_userid()
                while True:
                
                    if unique_id not in existing_ids:
                        user.userid = unique_id
                        break
                    else:
                        unique_id = generate_userid()
                
                user.save()
                user = Client.objects.get(userid=unique_id)
                new_username = user.username + ''.join(random.choice(string.digits) for _ in range(5))
                user.username = new_username
                user.save()
                # Send email
                # subject = 'Your User ID'
                # message = f'Your User ID is: {unique_id}'
                # from_email = EMAIL_HOST_USER
                # recipient_list = [user.email]
                # print(from_email)

                # try:
                #     send_mail(subject, message, from_email, recipient_list)
                # except BadHeaderError as b:
                #     print(b)

                messages.success(request, 'Registration successful. You can now login.')
                return redirect('userlogin')
            
        except Exception as e:
           print(e)
    else:
        form = cr()

    return render(request, 'registration.html', {'form': form})

def loginForm(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        usertype=request.POST.get('usertype')
        user=Client.objects.filter(userid=userid)
        userobject = authenticate(userid=userid, password=password)
        if userobject is not None:
            if usertype=='Farmer':
                login(request, userobject)
                return redirect('home')
            else:
                pass
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html', {'form': cl()})

def logoutUser(request):
    request.session.flush()
    logout(request)
    return redirect('userlogin')
