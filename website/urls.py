from django.urls import path

from .Views import viewHandler

urlpatterns = [
    path("", viewHandler.index),
    path("tags", viewHandler.tags),
    path("tags/<str:tag>/adverts", viewHandler.adverts),
    path("adverts/<int:id>", viewHandler.advert),
    path("adverts/create", viewHandler.createAdvert),
    path("user/<str:userId>", viewHandler.user),
    path("users", viewHandler.users)
]
