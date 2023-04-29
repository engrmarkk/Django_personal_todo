from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('todo', views.index, name='index'),
    path('delete/<todo_id>/', views.delete_todo, name='delete_todo'),
    path('complete/<todo_id>/', views.complete_todo, name='complete_todo'),
    path('logout', views.logout, name='logout'),
]
