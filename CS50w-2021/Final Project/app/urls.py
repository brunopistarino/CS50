from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register-login", views.register_login, name="register-login"),
    path("user_logout", views.user_logout, name="user_logout"),
    path("main_view", views.main_view, name="main_view"),
    path("get_project/<int:project_id>", views.get_project, name="get_project"),
    path("get_tasks/<int:project_id>", views.get_tasks, name="get_tasks"),
    path("task_complete_uncomplete/<str:action>/<int:task_id>", views.task_complete_uncomplete, name="task_complete_uncomplete"),
    path("get_user/<str:user_id>", views.get_user, name="get_user"),
    path("get_all_users", views.get_all_users, name="get_all_users"),
    path("create_task", views.create_task, name="create_task"),
    path("create_chat", views.create_chat, name="create_chat"),
    path("create_project", views.create_project, name="create_project"),
    path("edit_project", views.edit_project, name="edit_project"),
    path("delete_project", views.delete_project, name="delete_project"),
    path("get_tasks_by_project/<int:project_id>", views.get_tasks_by_project, name="get_tasks_by_project"),
    path("get_chats_by_project/<int:project_id>", views.get_chats_by_project, name="get_chats_by_project"),
    path("get_user_all_tasks", views.get_user_all_tasks, name="get_user_all_tasks"),
    path("get_user_id_by_username/<str:username>", views.get_user_id_by_username, name="get_user_id_by_username"),
    path("is_current_user_owner/<int:project_id>", views.is_current_user_owner, name="is_current_user_owner")
]
