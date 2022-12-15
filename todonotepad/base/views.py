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
from django.db.models import Q
from .forms import NoteForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url="MainLogin")
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

#todo views.


class Todolist(ListView, LoginRequiredMixin):
    model = Todo
    context_object_name = 'todos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos'] = context['todos'].filter(host=self.request.user)
        context['count'] = context['todos'].filter(completed=True).count()

        input_search = self.request.GET.get('q') if self.request.GET.get("q") != None else None
        if input_search:
            context['todos'] = context['todos'].filter(
                title__contains=input_search)

        context['input_search'] = input_search

        return context
    
    
class TodoDelete(DeleteView, LoginRequiredMixin):
    model = Todo
    context_object_name = 'todoDelete'
    success_url = reverse_lazy("todotasks")
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(host=owner)


class TodoCreate(CreateView, LoginRequiredMixin):
    model = Todo
    template_name = 'base/createTodo.html'
    fields = ['title', 'completed']
    success_url = reverse_lazy('todotasks')
    def form_valid(self, form):
        form.instance.host = self.request.user
        return super(TodoCreate, self).form_valid(form)
    

class TodoUpdate(UpdateView, LoginRequiredMixin):
    model = Todo
    fields = ["title", "completed"]
    success_url = reverse_lazy('todotasks')

#notepad views


@login_required(login_url="MainLogin")
def notepadHome(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    notepad = Notepad.objects.filter(
        Q(title__icontains=q) | Q(body__icontains=q))
    note_count = notepad.count()
    context = {'notepad': notepad, 'note_count': note_count}
    return render(request, 'base/notepadHome.html', context)    

            
@login_required(login_url="MainLogin")
def notepadRoom(request, pk):
    notepad = Notepad.objects.get(id=pk)
    if notepad.host != request.user:
        return HttpResponse('You are not authorized to this page')
    notepad = Notepad.objects.get(id=pk)
    context = {'notepad': notepad}
    return render(request,'base/notepadRoom.html', context)


@login_required(login_url="MainLogin")
def notepadCreate(request):
    form = NoteForm()
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notepadHome')
    context = {'form': form}
    return render(request,'base/notepadCreate.html', context)


@login_required(login_url="MainLogin")
def notepadUpdate(request, pk):
    notepad = Notepad.objects.get(id=pk)
    if notepad.host != request.user:
        return HttpResponse('you are not authorize on this page')
    form = NoteForm()
    if request.method == "POST":
        form = NoteForm(request.POST, instance = notepad)
        if form.is_valid():
            form.save()
            return redirect('notepadHome')
    context = {'form': form}
    return render(request,'base/notepadCreate.html', context)


@login_required(login_url="MainLogin")
def notepadDelete(request, pk):
    notepad = Notepad.objects.get(id=pk)
    if notepad.host != request.user:
        return HttpResponse('you are not authorized in this page')
    if request.method == "POST":
        notepad.delete()
        return redirect('notepadHome')
    return render(request, 'base/notepadDelete.html', {})