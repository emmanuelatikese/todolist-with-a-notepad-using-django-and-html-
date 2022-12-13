
from django.urls import path
from .import views
from .views import Todolist, TodoDelete, TodoCreate, TodoUpdate, MainRegister, MainLogin
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.mainHome, name='MainHome'),
    path('todolist/', Todolist.as_view(), name='todotasks'),
    path('tododelete/<str:pk>/', TodoDelete.as_view(), name='Tododelete'),
    path('todoCreate/', TodoCreate.as_view(), name='todoCreate'),
    path('todoUpdate/', TodoUpdate.as_view(), name='todoUpdate'),
    path('MainRegister/', MainRegister.as_view(), name='MainRegister'),
    path('MainLogin/', MainLogin.as_view(), name='MainLogin'),
    path('LogoutView', LogoutView.as_view(next_page='MainLogin'), name='Logout'),
    # Now the paths for the notepad
    
]
