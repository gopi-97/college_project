from django.shortcuts import render
from django.shortcuts import render
from manage_account.models import Farmer
from manage_account.urls import *
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def load_dash(request):
    username=request.session.get('username')
    user = Farmer.objects.get(username =username)
    profile_pic = user.profile_pic.url
    return render(request,'dashboard/dashboard.html',{'user_id':username,'profile_pic':profile_pic})


@login_required
def riceCultivation(request):
    return render(request,'dashboard/research_rice_cultivation.html')


@login_required
def cultivationPractice(request):
    return render(request,'dashboard/cultivation_practice.html')


@login_required
def cropConsultants(request):
    return render(request,'dashboard/crop_consultant.html')

@login_required
def externalLinks(request):
    return render(request,'dashboard/external_link.html')


@login_required
def diseaseAndPests(request):
    return render(request,'dashboard/disease_and_pests.html')


@login_required
def commingSoon(request):
    return render(request,'dashboard/comming_soon.html')