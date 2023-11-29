from django.shortcuts import render

# Create your views here.

def load_dash(request):
    return render(request,'dashboard/dashboard.html')
