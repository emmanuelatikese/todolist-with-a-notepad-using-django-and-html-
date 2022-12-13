from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Todo, Notepad
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy


def mainHome(request):
    return render(request, 'base/home.html',{})


class MainRegister(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('MainHome')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return super(MainRegister, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('MainHome')
        return super(MainRegister, self).get(*args, **kwargs)


class MainLogin(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('MainHome')


class Todolist(ListView):
    model = Todo
    context_object_name = 'todos'
    
    
    
class TodoDelete(DeleteView):
    model = Todo
    context_object_name = 'todoDelete'
    success_url = reverse_lazy("todotasks")
    #Don't forget to add something 

class TodoCreate(CreateView):
    model = Todo
    template_name = 'base/createTodo.html'
    fields = ['title', 'completed']
    success_url = reverse_lazy('todotasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreate, self).form_valid(form)
    

class TodoUpdate(UpdateView):
    model = Todo
    fields = ["title", "completed"]
    success_url = reverse_lazy('todotasks')


    
    

            
