from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Todo


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('/todo')
    # if you are sending a post request
    if request.method == 'POST':
        # get the username from the form
        username = request.POST.get('username')
        # get the password from the form
        password = request.POST.get('password')
        # check if the user exist
        user_exist = User.objects.filter(username=username).exists()
        # if the user exist
        if user_exist:
            # check if the password sent is the password associated with the username
            user = authenticate(username=username, password=password)
            # if yes
            if user:
                # login the user
                auth.login(request, user)
                # and redirect the user to the todo route
                return redirect('/todo')
            # if the password is wrong, then flash the user this message and still stay on same page
            messages.info(request, "wrong password")
            return redirect("/")
        # if the username doesn't exist, display the 'wrong username' message
        messages.info(request, "wrong username")
    # this is for the get request, this loads the login.html template when requested for
    return render(request, 'login.html')


# the method with the login required decorator can only be accessed by an authenticated user
@login_required()
def index(request):
    # query the database for the todos that are yet to be completed
    all_todos = Todo.objects.all().filter(completed=False)
    # query the database for the todos that completed
    alltodos = Todo.objects.all().filter(completed=True)
    # save in a context dictionary
    context = {
        'todos': all_todos,
        'todoss': alltodos
    }
    # if a post request is being sent to this route
    if request.method == 'POST':
        # get the todo content from the form
        todo = request.POST.get('todo')
        # if it's an empty data
        if not todo:
            # display this message to the user
            messages.info(request, 'Empty todo')
            return redirect('/todo')
        # if the data sent is not empty, save it in the database
        new_todo = Todo(todo=todo)
        new_todo.save()
        return redirect("/todo")
        # messages.info(request, 'Todo added')
    # for the get request, we send the context dictionary to the template for usage
    return render(request, 'index.html', context)


@login_required()
def delete_todo(request, todo_id):
    # the todo_id will be sent from the template file
    # get the todo with that particular id from the database
    todo = Todo.objects.get(id=todo_id)
    # delete the todo
    todo.delete()
    # redirect the user to that same page, i.e, the todo page
    return redirect('/todo')


@login_required()
def complete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    # get the todo and update the completed column to True so as to get it completed
    todo.completed = True
    # update and save the new data
    todo.save()
    return redirect('/todo')


# @login_required()
# def logout(request):
#     # logout the user
#     auth.logout(request)
#     messages.error(request, 'You have been logged out')
#     # redirect the user to the login page
#     return redirect('/')
