from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('tasklist/',TaskList.as_view(),name='tasks'),#home url
    path('task/<int:pk>/',TaskDetail.as_view(),name='tasks-detail'),
    path('task-create/',TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',TaskDelete.as_view(),name='task-delete'),

]

'''
Since URL configurations expects callable function rather than class,
 we will use .as_view() class method of our View because as_view() returns 
 a function to be used with URLs. 
 
 This function does series of work for us,

1. calls setup() method to initialize the attributes
2. calls dispatch() method which determines if request if GET or POST and send this request to corresponding request method

other example:
                from django.views import View
                class DashboardView(View):
                    def get(self, request):
                        # GET method 
                        pass
                    def post(self, request):
                        # POST method
                        pass
'''