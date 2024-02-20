from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import JsonResponse
from manage_account.models import Farmer
from manage_account.urls import *
from .models import FarmerInventory,InventoryGallery
from cultivation.models import CurrentCultivation
import plotly.graph_objs as go
import plotly.offline as opy
from collections import defaultdict
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse
import base64
# from .forms import CustomInventoryUpdateForm
# Create your views here.




def generate_bar_chart(request):
    #fetching cultivation details of current user
    username = request.session.get('username')
    
    val = FarmerInventory.objects.filter(user_id=username)#user_id is used for model reference 

    product_quantities = defaultdict(list)

    for item in val:
        product_quantities[item.product].append(item.quantity)

    # If you want to convert quantity strings to integers
    for product, quantities in product_quantities.items():
        product_quantities[product] = [int(qty.replace('kg', '')) for qty in quantities]

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


class InventoryList(LoginRequiredMixin,ListView):
    model = FarmerInventory
    context_object_name = 'InventoryList'
    template_name = 'inventory/inventory_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        username = self.request.session.get('username')
        dataset = FarmerInventory.objects.filter(user_id = username)[:4]
        return dataset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return super().get_context_data(**kwargs)


class FullInventoryList(LoginRequiredMixin,ListView):
    model = FarmerInventory
    context_object_name = 'InventoryList'
    template_name = 'inventory/full_inventory_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        username = self.request.session.get('username')
        dataset = FarmerInventory.objects.filter(user_id = username)
        return dataset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return super().get_context_data(**kwargs)




class InventoryDetail(LoginRequiredMixin, DetailView):
    model = FarmerInventory
    template_name = 'inventory/inventory_detail.html'
    context_object_name = 'inventory'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(FarmerInventory, pk=pk)



def inventoryGallery(request):
    user = request.session.get('username')
    userData = FarmerInventory.objects.filter(user_id=user)
    gallery_images = []
    for item in userData:
        for gallery_item in item.gallery.all():
            # Read image data from the ImageFieldFile object
            with gallery_item.GalleryImage.open('rb') as f:
                image_data = f.read()
            # Convert image data to Base64 encoding
            base64_image = base64.b64encode(image_data).decode('utf-8')
            gallery_images.append(base64_image)
    context = {'inventoryImages': gallery_images}
    return render(request, 'inventory/inventory_gallery.html', context)



class InventoryUpdate(LoginRequiredMixin,UpdateView):
    model = FarmerInventory
    context_object_name = 'inventory'
    # form_class = CustomInventoryUpdateForm
    fields = ['product', 'quantity', 'image']

    template_name = 'inventory/inventory_update.html'
   


    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(FarmerInventory, pk=pk)
    

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('inventory-detail', kwargs={'pk': pk})
    
    def post(self,request,*args,**kwargs):
        inventory = FarmerInventory.objects.create(
            user=request.user,
            product=request.product,
            product_id = request.product_id,
            quantity=request.POST.get('quantity'),
            image=request.FILES.get('image'),
            gallery=request.FILES.get('gallery'),

        )

        inventory.save()


class InventoryItemDelete(LoginRequiredMixin,DeleteView):
    model=FarmerInventory
    success_url=reverse_lazy('inventory-list-full')
    context_object_name='cultivation'


