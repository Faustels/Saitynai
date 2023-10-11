from django.urls import path

from .Views import users, tags, adverts, comments

urlpatterns = [
    path("user/allUsers", users.users),
    path("user/<str:name>", users.user),
    path("user/createUser", users.createUser),

    path("tag/tags", tags.tags),
    path("tag/<str:name>", tags.tag),
    path("tag/createTag", tags.createTag),

    path("advert/allAdverts", adverts.allAdverts),
    path("advert/<int:advert>", adverts.advert),
    path("advert/createAdvert", adverts.createAdvert),
    path("advert/tag/<str:tag>", adverts.advertByTag),

    path("comment/allComments", comments.allComments),
    path("comment/<int:id>", comments.comment),
    path("comment/advert/<int:advert>", comments.commentsByAdvert),
    path("comment/createComment", comments.createComment),
    path("comment/tag/<str:tag>", comments.commentsByTag),
]