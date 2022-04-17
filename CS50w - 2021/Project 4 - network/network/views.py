from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

from .models import User, Posts, Follows

def index(request):
    return render(request, "network/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def paginate(posts, current_page_number):
    posts = posts.order_by("-timestamp").all()
    pagination = Paginator(posts, 10)
    posts_list = pagination.page(current_page_number).object_list
    current_page = pagination.page(current_page_number)
    has_next = current_page.has_next()
    has_previous = current_page.has_previous()
    return posts_list, has_next, has_previous

def posts(request, current_page_number):
    posts = Posts.objects.all()

    posts_list, has_next, has_previous = paginate(posts, current_page_number)

    return JsonResponse({"posts": [post.serialize() for post in posts_list], "has_next": has_next, "current_page_number": current_page_number, "has_previous": has_previous}, safe=False)

def following_posts(request, current_page_number):
    user = request.user
    following = user.following.all().values('following_user')
    posts = Posts.objects.filter(user__in=following)

    posts_list, has_next, has_previous = paginate(posts, current_page_number)

    return JsonResponse({"posts": [post.serialize() for post in posts_list], "has_next": has_next, "current_page_number": current_page_number, "has_previous": has_previous}, safe=False)

def profile(request, user, current_page_number):
    try:
        profile = User.objects.get(username=user)
        posts = Posts.objects.filter(user=profile)
    except User.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=404)

    try:
        if request.user.is_authenticated:
            Follows.objects.get(user=request.user, following_user=profile)
            check_follow = True
        else:
            check_follow = False
    except Follows.DoesNotExist:
        check_follow = False

    posts_list, has_next, has_previous = paginate(posts, current_page_number)

    return JsonResponse({'current_user': request.user.username,'username': user, "following": profile.following.all().count(), "followers": profile.followers.all().count(), 'check_follow': check_follow, 'posts': [post.serialize() for post in posts_list], "has_next": has_next, "current_page_number": current_page_number, "has_previous": has_previous})

@csrf_exempt
@login_required
def create(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    content = data.get("content", "")

    post = Posts(user=request.user, content=content)
    post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)

def like(request, post_id):
    post = Posts.objects.get(id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    amount = post.likes.count()
    return JsonResponse({"amount": amount})

def like_state(request, post_id):
    post = Posts.objects.get(id=post_id)
    if request.user in post.likes.all():
        return JsonResponse({"state": True})
    else:
        return JsonResponse({"state": False})

def follow(request, profile_user):
    user = request.user
    profile_user = User.objects.get(username=profile_user)

    try:
        Follows.objects.get(user=user, following_user=profile_user)
        check_follow = True
    except Follows.DoesNotExist:
        check_follow = False

    if check_follow == False:
        Follows.objects.create(user=user, following_user=profile_user)
    else:
        Follows.objects.get(user=user, following_user=profile_user).delete()

    return JsonResponse({"state": check_follow, "followers": profile_user.followers.all().count()}, status=200)

@csrf_exempt
def edit(request, post_id, type):
    user = request.user
    post = Posts.objects.get(id=post_id)
    owner = post.user

    if type == 1:
        if user == owner:
            return JsonResponse({"owner": True})
        else:
            return JsonResponse({"owner": False})

    elif type == 2:
        if request.method == "PUT":
            if user == owner:
                data = json.loads(request.body)
                post.content = data["content"]
                post.save()
                return JsonResponse({"message": "Success"}, status=200)
            else:
                return JsonResponse({"error": "Validation failed"}, status=400)
        else:
            return JsonResponse({"error": "PUT request required."}, status=400)

    else:
        return JsonResponse({"message": "error"}, status=404)

def user_authentication(request):
    if request.user.is_authenticated:
        authentication = True
    else:
        authentication = False
    return JsonResponse({"authentication": authentication}, status=200)