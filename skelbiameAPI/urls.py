from django.urls import path

from .Views import users, tags, adverts, comments, ratings

urlpatterns = [
    path("users", users.users),
    path("users/<str:name>", users.user),

    path("tags", tags.tags),
    path("tags/<str:name>", tags.tag),

    path("adverts", adverts.allAdverts),
    path("adverts/<int:advert>", adverts.advert),
    path("tags/<str:tag>/adverts", adverts.advertByTag),

    path("comments", comments.allComments),
    path("comments/<int:id>", comments.comment),
    path("adverts/<int:advert>/comments", comments.commentsByAdvert),
    path("tags/<str:tag>/comments", comments.commentsByTag),

    path("adverts/<int:advert>/ratings", ratings.ratingOfAdvert),
    path("adverts/<int:advert>/ratings/list", ratings.advertRatingList),
    path("ratings/<int:id>", ratings.rating),
]