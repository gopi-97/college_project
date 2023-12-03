from django.shortcuts import render
from manage_account.models import Client
from .form import addProductForm
from .models import Cultivation
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def loadHome(request,user):
    return render(request,'dashboard/home.html')


def add_product(request):
    if request.method=="POST":
        try:
            form=addProductForm
            if form.is_valid():
                Cultivation=form.save(commit=True)
            else:
               return render(request,'dashboard/dashboard.html')
        except Exception as e:
            print(e)




def load_dash(request):
    return render(request,'dashboard/dashboard.html')