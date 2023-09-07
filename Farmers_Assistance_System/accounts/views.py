from django.shortcuts import render
import uuid
from .forms import Userforms
from django.contrib import messages
# Create your views here.

def homepage(request):
    return render(request,'accounts/index.html')

def add_user(request):
    if request.method == 'POST':
        form = Userforms(request.POST)
        if form.is_valid():
            form.save()
            return messages.success(request,"successfully added")
        
    else:
        form = Userforms()
    return render(request, 'signup.html', {'form': form})