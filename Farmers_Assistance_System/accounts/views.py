from django.shortcuts import render,redirect
import uuid
from .forms import Userforms
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import Users
from django.http import JsonResponse
# Create your views here.

def homepage(request):
    return render(request,'accounts/index.html')

def generate_unique_userid(request):
    # Generate a unique user ID
    while True:
        generated_userid = get_random_string(length=10)
        if not Users.objects.filter(userid=generated_userid).exists():
            break
        
    # Split the ID into three parts
    formatted_userid = '-'.join([generated_userid[i:i+4] for i in range(0, len(generated_userid), 4)])
   # Return JSON response
    return JsonResponse({'formatted_userid': formatted_userid})

def add_user(request):
    if request.method == 'POST':
        form = Userforms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added")
            return redirect('home')  # Redirect to the login page
    else:
        form = Userforms()
    return render(request, 'signup.html', {'form': form})