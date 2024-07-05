from django.contrib import admin
from .models import User, Projects, Tasks, Chats

# Register your models here.
admin.site.register(User)
admin.site.register(Projects)
admin.site.register(Tasks)
admin.site.register(Chats)