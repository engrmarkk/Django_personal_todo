from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Todo


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_exist = User.objects.filter(username=username).exists()
        if user_exist:
            user = authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('/todo')
            messages.info(request, "wrong password")
            return redirect("/")
        messages.info(request, "wrong username")
    return render(request, 'login.html')


@login_required()
def index(request):
    all_todos = Todo.objects.all().filter(completed=False)
    alltodos = Todo.objects.all().filter(completed=True)
    context = {
        'todos': all_todos,
        'todoss': alltodos
    }
    if request.method == 'POST':
        todo = request.POST.get('todo')
        if not todo:
            messages.info(request, 'Empty todo')
            return redirect('/todo')
        new_todo = Todo(todo=todo)
        new_todo.save()
        # messages.info(request, 'Todo added')
    return render(request, 'index.html', context)


def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return redirect('/todo')


def complete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.completed = True
    todo.save()
    return redirect('/todo')
