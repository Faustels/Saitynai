from django.urls import path

from .Views import user, tags

urlpatterns = [
    path("users", user.users),
    path("user/<str:name>", user.user),
    path("createUser", user.createUser),
    path("tags", tags.tags),
    path("tag/<str:name>", tags.tag),
    path("createTag", tags.createTag),
]