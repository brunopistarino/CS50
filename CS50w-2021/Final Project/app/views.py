from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, request
from django.urls import reverse
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import json

from .models import User, Projects, Tasks, Chats

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "app/main/index.html")
    else:
        return render(request, "app/landing/landing.html")

def register_login(request):
    if request.method == "POST" and 'register' in request.POST:
        username = request.POST["register_username"]
        first_name = request.POST["register_firstname"]
        last_name = request.POST["register_lastname"]
        email = request.POST["register_email"]
        password = request.POST["register_password"]
        confirm_password = request.POST["register_confirm"]
        if password != confirm_password:
            return render(request, "app/landing/register-login.html", {"message": "Passwords must match."})

        if username == "" or first_name == "" or last_name == "" or email == "" or password == "" or confirm_password == "":
            return render(request, "app/landing/register-login.html", {"message": "All entries must be completed."})

        try:
            user = User.objects.create_user(username, email, password , first_name=first_name, last_name=last_name)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            return render(request, "app/landing/register-login.html", {"message": "Username already taken."})

    if request.method == "POST" and 'login' in request.POST:
        username = request.POST["login_username"]
        password = request.POST["login_password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    return render(request, "app/landing/register-login.html")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def main_view(request):
    user = request.user
    tasks = Tasks.objects.filter(user=user)

    today_tasks = tasks.filter(date=date.today())

    tasks_completed = today_tasks.filter(completed=True).count()
    tasks_left = today_tasks.filter(completed=False).count()
    tasks_for_the_week = tasks.filter(date__range=[date.today(), date.today() + timedelta(days=6)]).count()
    projects = Projects.objects.filter(members=user)
    serialized_projects = serializers.serialize('json', projects)
    serialized_tasks = serializers.serialize('json', today_tasks)
    return JsonResponse({"first_name": user.first_name, "user_pk": user.id, "projects": serialized_projects, "tasks": serialized_tasks, "tasks_completed": tasks_completed, "tasks_left": tasks_left, "tasks_for_the_week": tasks_for_the_week})

def get_project(request, project_id):
    project = Projects.objects.filter(id=project_id)
    serialized_project = serializers.serialize('json', project)
    return JsonResponse({"project": serialized_project})

def get_tasks(request, project_id):
    project = Projects.objects.get(id=project_id)
    tasks = Tasks.objects.filter(project=project)
    pending_tasks = tasks.filter(completed=False)
    pending_tasks_count = pending_tasks.count()
    return JsonResponse({"pending_tasks": pending_tasks_count})

def get_tasks_by_project(request, project_id):
    project = Projects.objects.get(id=project_id)
    tasks = Tasks.objects.filter(project=project).order_by('date')
    serialized_tasks = serializers.serialize('json', tasks)
    return JsonResponse({"tasks": serialized_tasks, "actual_date": date.today()})

def get_user(request, user_id):
    user = User.objects.get(id=user_id)
    return JsonResponse({"username": user.username, "id": user.pk, "first_name": user.first_name, "last_name": user.last_name})

def get_user_id_by_username(request, username):
    user = User.objects.get(username=username)
    return JsonResponse({"id": user.pk})

def get_all_users(request):
    users = User.objects.all()
    current_user = request.user
    serialized_users = serializers.serialize('json', users)
    return JsonResponse({"users": serialized_users, "current_user_username": current_user.username, "current_user_first_name": current_user.first_name, "current_user_last_name": current_user.last_name, "current_user_email": current_user.email, "current_user_pk": current_user.id})

def get_chats_by_project(request, project_id):
    project = Projects.objects.get(id=project_id)
    chats = Chats.objects.filter(project=project)
    serialized_chats = serializers.serialize('json', chats)
    return JsonResponse({"chats": serialized_chats, "current_user_id": request.user.id})

def get_user_all_tasks(request):
    user = request.user
    tasks = Tasks.objects.filter(user=user)
    serialized_tasks = serializers.serialize('json', tasks)
    return JsonResponse({"tasks": serialized_tasks})

def is_current_user_owner(request, project_id):
    project = Projects.objects.get(id=project_id)
    if request.user == project.owner:
        response = True
    else:
        response = False
    return JsonResponse({"response": response})


def task_complete_uncomplete(request, action, task_id):
    task = Tasks.objects.get(id=task_id)

    if action == "complete":
        task.completed = True
        task.save()
    else:
        task.completed = False
        task.save()

    return JsonResponse({"message": "success"})

@csrf_exempt
@login_required
def create_task(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    name = data.get("name", "")
    user = User.objects.get(id=data.get("user_id", ""))
    project = Projects.objects.get(id=data.get("project_id", ""))
    date = data.get("date", "")
    Tasks.objects.create(name=name, project=project, date=date, user=user)

    return JsonResponse({"message": "Task created successfully"}, status=201)

@csrf_exempt
@login_required
def create_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    message = data.get("message", "")
    project_id = data.get("project_id", "")
    project = Projects.objects.get(id=project_id)
    user = request.user
    Chats.objects.create(user=user, project=project, message=message)

    return JsonResponse({"message": "Chat created successfully"}, status=201)

@csrf_exempt
@login_required
def create_project(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request requiered."}, status=400)
    
    data = json.loads(request.body)
    name = data.get("name", "")
    owner = request.user
    members = data.get("members", "")
    color = data.get("color", "")

    members.append(owner.username)

    project = Projects.objects.create(name=name, owner=owner, color=color)

    for member in members:
        user = User.objects.get(username=member)
        project.members.add(user)

    return JsonResponse({"message": "Project created successfully"}, status=201)

@csrf_exempt
@login_required
def edit_project(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request requiered."}, status=400)

    data = json.loads(request.body)
    project_id = data.get("project_id", "")
    edited_members_usernames = data.get("members", "")
    project = Projects.objects.get(id=project_id)
    project_members = Projects.objects.get(id=project_id).members.all()
    
    original_members_usernames = []
    for member in project_members:
        if member != request.user:
            original_members_usernames.append(member.username)

    members_usernames_to_add = list(set(edited_members_usernames) - set(original_members_usernames))
    members_usernames_to_remove = list(set(original_members_usernames) - set(edited_members_usernames))

    for username_to_add in members_usernames_to_add:
        user_to_add = User.objects.get(username=username_to_add)
        project.members.add(user_to_add)

    for username_to_remove in members_usernames_to_remove:
        user_to_remove = User.objects.get(username=username_to_remove)
        project.members.remove(user_to_remove)

    return JsonResponse({"message": "Project edited successfully"}, status=201)

@csrf_exempt
@login_required
def delete_project(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request requiered."}, status=400)

    data = json.loads(request.body)
    project_id = data.get("project_id", "")
    project = Projects.objects.get(id=project_id)
    project.delete()

    return JsonResponse({"message": "Project deleted successfully"}, status=201)