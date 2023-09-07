from django.shortcuts import render
import uuid
# Create your views here.

def homepage(request):
    return render(request,'accounts/index.html')

