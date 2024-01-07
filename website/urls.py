from django.urls import path

from .Views import viewHandler

urlpatterns = [
    path("", viewHandler.index),
    path("tags", viewHandler.tags),
    path("tags/<str:tag>/adverts", viewHandler.adverts),
    path("adverts/<int:id>", viewHandler.advert)
]
