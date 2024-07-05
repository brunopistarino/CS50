
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("posts/<int:current_page_number>", views.posts, name="posts"),
    path("following/<int:current_page_number>", views.following_posts, name="following_posts"),
    path("posts/create", views.create, name="create"),
    path("profile/<str:user>/<int:current_page_number>", views.profile, name="profile"),
    path("like/<int:post_id>", views.like, name="like"),
    path("like/state/<int:post_id>", views.like_state, name="like_state"),
    path("follow/<str:profile_user>", views.follow, name="follow"),
    path("edit/<int:post_id>/<int:type>", views.edit, name="edit"),
    path("authentication", views.user_authentication, name="authentication"),
]
