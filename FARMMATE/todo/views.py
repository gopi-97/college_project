from typing import Any
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse,request
from .models import Tasks
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin #prevents users who are not logged in from accessing services
# Create your views here.


class TaskList(LoginRequiredMixin,ListView):
    model=Tasks
    context_object_name='tasks'
    template_name = 'todo/tasks_list.html'

    def get_queryset(self):
        # Filter tasks related to the logged-in user
        username = self.request.session.get('username')
        return Tasks.objects.filter(user_id=username)[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Count incomplete tasks for the logged-in user
        context['count'] = self.get_queryset().filter(complete=False).count()

        search_input=self.request.GET.get('searchbar') or ''
        if search_input:
            # returns tasks whose title contains the search word , we can change icontains to startswith and more
            context['tasks']=context['tasks'].filter(title__icontains=search_input)
            context['search_input']=search_input
        return context

class FullTaskList(LoginRequiredMixin,ListView):
    model=Tasks
    context_object_name='tasks'
    template_name = 'todo/full_task_list.html'

    def get_queryset(self):
        # Filter tasks related to the logged-in user
        username = self.request.session.get('username')
        return Tasks.objects.filter(user_id=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Count incomplete tasks for the logged-in user
        context['count'] = self.get_queryset().filter(complete=False).count()

        search_input=self.request.GET.get('searchbar') or ''
        if search_input:
            # returns tasks whose title contains the search word , we can change icontains to startswith and more
            context['tasks']=context['tasks'].filter(title__icontains=search_input)
            context['search_input']=search_input
        return context


class TaskDetail(LoginRequiredMixin,DetailView):
     model=Tasks
     context_object_name='task'
     template_name='todo/task.html'


class TaskCreate(LoginRequiredMixin,CreateView):
     model=Tasks
     fields=['title','description','complete']# for every field use '__all__'
     success_url=reverse_lazy('tasks')#home url

     def form_valid(self,form):
        form.instance.user=self.request.user #setting the user as current logged in user when submitting forms 
        return super(TaskCreate,self).form_valid(form)#this sets the user field of constructor of TaskCreate class as the current user
        ''' 
          we specify the class inside the return function because 
         we want to call the form_valid() method of the parent class,
          This method performs some validations and saves the form data to the database. 
          By using super(), we can access the inherited method without repeating the code or hardcoding the class name.
        '''


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Tasks
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')#home url


class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Tasks
    success_url=reverse_lazy('tasks')#home url
    context_object_name='task'
