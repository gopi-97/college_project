from typing import Any
from django.shortcuts import render
from manage_account.models import Farmer
from manage_account.urls import *
from .models import Cultivation,CurrentCultivation,Farms
from inventory.models import FarmerInventory
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random
from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse
# Create your views here.



def generate_product_id(start_date,product):
    day = str(start_date.day)
    random_num = str(random.randint(0, 100))
    product_id = f"{product}{day}{random_num}"
    return product_id



@login_required
@csrf_protect
def add_product(request):

    if request.method=="POST":
        try:
            username=request.session.get('username')
            client_instance = Farmer.objects.get(username=username)
            product=request.POST['product']
            location=request.POST['location']
            cultivated_area=request.POST['cultivated_area']
            start_date=request.POST['start_date']
            date_object = datetime.strptime(start_date, f'%Y-%m-%dT%H:%M')# RuntimeWarning: DateTimeField Cultivation.start_date received a naive datetime (2023-12-15 15:22:00) while time zone support is active.
            # # Convert the naive datetime to an aware datetime
            date_object_aware = timezone.make_aware(date_object)
            description=request.POST['description']
            productid=generate_product_id(date_object,product)

             # Creating an instance of Cultivation and saving it
            cultivation = CurrentCultivation(
                user=client_instance,
                product=product,
                product_id=productid,
                location=location,
                cultivated_area=cultivated_area,
                start_date=date_object_aware,
                description=description
            )
            cultivation.save()  
            script = """
            <script>
                alert(" added to current cultivation successfully!");
                window.location.href = "{0}";
            </script>
            """.format(reverse('dashboard'))
                
            return HttpResponse(script)

        except Exception as e:
            print(e)
    return render(request,'cultivation/add_product.html')


class addToInventory(LoginRequiredMixin,UpdateView):
    model = FarmerInventory
    fields =[]
    context_object_name = 'currentcul'
    template_name = 'cultivation/current_cultivation_update.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(FarmerInventory, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming you have logic to get the currentcul object
        return context

    def post(self,request,*args,**kwargs):

        # CurrentCultivation model stores current cultivations and Cultivation model stores entire cultivation history
        current_cultivation = CurrentCultivation.objects.get(id=self.kwargs.get('pk'))#accessing the id of the cultivation
        #adding the details to the history table
        cultivation = Cultivation.objects.create(
            user=request.user,
            product=current_cultivation.product,
            product_id=current_cultivation.product_id,
            location=current_cultivation.location,
            cultivated_area=current_cultivation.cultivated_area,
            start_date=current_cultivation.start_date,
            description=current_cultivation.description,
            status='harvested',
            harvested_date=request.POST.get('harvested_date')
        )
        cultivation.save()

        inventory = FarmerInventory.objects.create(
            user=request.user,
            product=current_cultivation.product,
            product_id = current_cultivation.product_id,
            quantity=request.POST.get('quantity'),
            images=request.FILES.get('images')
        )
        inventory.save()

        # Delete the record from CurrentCultivation 
        current_cultivation.delete()

        script = """
    <script>
        alert("product added to Inventory  successfully!");
        window.location.href = "{0}";
    </script>
    """.format(reverse('dashboard'))
        
        return HttpResponse(script)


    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('cultivation-detail', kwargs={'pk': pk})

class currentCultivationDetail(LoginRequiredMixin, DetailView):
    model = CurrentCultivation
    template_name = 'cultivation/cultivation_detail.html'
    context_object_name = 'currentcultivation'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(CurrentCultivation, pk=pk)
    
    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('cultivation-detail', kwargs={'pk': pk})

# @login_required
# @csrf_protect
# def add_field(request):
#     if request.method=="POST":
#         try:
#             location=request.POST['location']
#             status=request.POST['status']
#             user=request.session.get('username')
#             client_instance = Farmer.objects.get(username=user)
#             farm=Farms(
#                 user=client_instance,
#                 location=location,
#                 status=status,
#             )
#             farm.save()
#             return render(request,'dashboard/dashboard.html')

#         except Exception as e:
#              print(e)
#     return render(request,'dashboard/dashboard.html')




class CultivationList(LoginRequiredMixin,ListView):
    model = Cultivation
    context_object_name = 'cultivationData'
    template_name = 'cultivation/cultivation_list.html'
    def get_queryset(self):
        username = self.request.session.get('username')
        dataset = Cultivation.objects.filter(user_id= username)
        return dataset
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
    
        return context
    

class CultivationShortList(LoginRequiredMixin,ListView):
    model = Cultivation
    context_object_name = 'cultivationData'
    template_name = 'cultivation/cultivationHistory.html'
    def get_queryset(self):
        username = self.request.session.get('username')
        dataset = Cultivation.objects.filter(user_id= username)[:3]
        return dataset
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
    
        return context
    
    '''
It looks like you might be mixing up the purpose of the get_context_data() method and the get_context_object_name() method. 
The get_context_object_name() method is used to define the context variable name for a single object in a DetailView and not typically used in a ListView'''

    # def get_context_object_name(self):
    #     return super().get_context_object_name('CultivationList',kwargs = self.get_context_data())




class CultivationDetail(LoginRequiredMixin, DetailView):
    model = Cultivation
    template_name = 'cultivation/cultivation_detail.html'
    context_object_name = 'cultivation'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Cultivation, pk=pk)




class CultivationUpdate(LoginRequiredMixin,UpdateView):
    model = Cultivation
    context_object_name = 'cultivation'
    template_name = 'cultivation/cultivation_update.html'
    fields = ['product','status','harvested_date','description']


    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Cultivation, pk=pk)
    

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('cultivation-detail', kwargs={'pk': pk})
    
    # def get_success_url(self,request):
    #     pk = self.kwargs.get('pk')
    #     return super().get_success_url(self,request,pk)

    '''
    The get_success_url() method in Django's UpdateView is used to redirect the user to a specific URL after a successful update. It should return the URL to which the user is redirected.
     get_success_url() does not take request as an argument. It's simply responsible for returning the URL to which the view will redirect upon successful form submission
    '''



class currentCultivation(LoginRequiredMixin,ListView):
    model = CurrentCultivation
    template_name = 'cultivation/currentCultivation.html'
    context_object_name = 'currentCultivation'

    def get_queryset(self):
        username = self.request.session.get('username')
        currentCul = CurrentCultivation.objects.filter(user_id=username)
        return currentCul
    
    def get_context_data(self, **kwargs: Any):
        return super().get_context_data()
    




