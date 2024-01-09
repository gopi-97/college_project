from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import JsonResponse
from manage_account.models import Farmer
from manage_account.urls import *
from .models import Cultivation,Farms,Inventory
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random
from datetime import datetime
from collections import defaultdict
import plotly.graph_objs as go
import plotly.offline as opy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse
# Create your views here.

@login_required
def load_dash(request):
    username=request.session.get('username')
    return render(request,'dashboard/dashboard.html',{'user_id':username})



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
            cultivation = Cultivation(
                user=client_instance,
                product=product,
                product_id=productid,
                location=location,
                cultivated_area=cultivated_area,
                start_date=date_object_aware,
                description=description
            )
            cultivation.save()  
            return render(request,'dashboard/dashboard.html')

        except Exception as e:
            print(e)
    return render(request,'dashboard/dashboard.html')



@login_required
@csrf_protect
def add_field(request):
    if request.method=="POST":
        try:
            location=request.POST['location']
            status=request.POST['status']
            user=request.session.get('username')
            client_instance = Farmer.objects.get(username=user)
            farm=Farms(
                user=client_instance,
                location=location,
                status=status,
            )
            farm.save()
            return render(request,'dashboard/dashboard.html')

        except Exception as e:
             print(e)
    return render(request,'dashboard/dashboard.html')




def generate_bar_chart(request):
    #fetching cultivation details of current user
    username = request.session.get('username')
    
    val = Inventory.objects.filter(user_id=username)#user_id is used for model reference 

    product_quantities = defaultdict(list)

    for item in val:
        product_quantities[item.product].append(item.quantity)

    # If you want to convert quantity strings to integers
    for product, quantities in product_quantities.items():
        product_quantities[product] = [int(qty.replace(' kg', '')) for qty in quantities]

    products=[]
    highest_harvests = []
    # simplified for loop
    for product, quantities in product_quantities.items():
        products.append(product)
        max_quantity = max(quantities)
        highest_harvests.append(max_quantity)

    # Create the bar chart using Plotly
    fig = go.Figure(data=[go.Bar(x=products, y=highest_harvests,marker=dict(color='green'))])
    fig.update_layout(
        xaxis =dict(title='Products'),
        yaxis = dict(title='Highest_yield (in kg)'),
    
    )
    chart_html = opy.plot(fig, auto_open=False, output_type='div')

    return JsonResponse({'chart_data': chart_html})


def graph_view(request):
    try:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'GET':
            username = request.session.get('username')
            chart_data = generate_bar_chart(request)
            return chart_data  # Return the response from generate_bar_chart directly
        else:
            # Handle other types of requests or return an error response
            return JsonResponse({'error': 'Invalid request'})
    except Exception as e:
        print(e)


class CultivationList(LoginRequiredMixin,ListView):
    model = Cultivation
    context_object_name = 'cultivationData'
    template_name = 'dashboard/partials/cultivation_list.html'
    def get_queryset(self):
        username = self.request.session.get('username')
        dataset = Cultivation.objects.filter(user_id= username)
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
    template_name = 'dashboard/partials/cultivation_detail.html'
    context_object_name = 'cultivation'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Cultivation, pk=pk)




class CultivationUpdate(LoginRequiredMixin,UpdateView):
    model = Cultivation
    context_object_name = 'cultivation'
    template_name = 'dashboard/partials/cultivation_update.html'
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



class InventoryList(LoginRequiredMixin,ListView):
    model = Inventory
    context_object_name = 'InventoryList'
    template_name = 'dashboard/partials/inventory_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        username = self.request.session.get('username')
        dataset = Inventory.objects.filter(user_id = username)[:4]
        return dataset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return super().get_context_data(**kwargs)


class FullInventoryList(LoginRequiredMixin,ListView):
    model = Inventory
    context_object_name = 'InventoryList'
    template_name = 'dashboard/partials/fullinventory_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        username = self.request.session.get('username')
        dataset = Inventory.objects.filter(user_id = username)
        return dataset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return super().get_context_data(**kwargs)




class InventoryDetail(LoginRequiredMixin, DetailView):
    model = Inventory
    template_name = 'dashboard/partials/inventory_detail.html'
    context_object_name = 'inventory'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Inventory, pk=pk)




class InventoryUpdate(LoginRequiredMixin,UpdateView):
    model = Inventory
    context_object_name = 'inventory'
    template_name = 'dashboard/partials/inventory_update.html'
    fields = ['product','quantity']


    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Inventory, pk=pk)
    

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('inventory-detail', kwargs={'pk': pk})


class InventoryItemDelete(LoginRequiredMixin,DeleteView):
    model=Inventory
    success_url=reverse_lazy('inventory-list-full')
    template_name = 'dashboard/partials/inventory_confirm_delete.html'
    context_object_name='cultivation'

