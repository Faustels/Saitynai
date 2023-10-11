from django.urls import path

from .Views import user, tags, adverts

urlpatterns = [
    path("user/allUsers", user.users),
    path("user/<str:name>", user.user),
    path("user/createUser", user.createUser),

    path("tag/tags", tags.tags),
    path("tag/<str:name>", tags.tag),
    path("tag/createTag", tags.createTag),

    path("advert/allAdverts", adverts.allAdverts),
    path("advert/<int:advert>", adverts.advert),
    path("advert/createAdvert", adverts.createAdvert),
    path("advert/tag/<str:tag>", adverts.advertByTag),
]