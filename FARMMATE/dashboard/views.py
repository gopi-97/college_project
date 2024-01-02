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
from django.shortcuts import render
from collections import defaultdict
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as opy




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
            status=request.POST['status']
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
                status=status,
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
    fig = go.Figure(data=[go.Bar(x=products, y=highest_harvests)])
   
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