from django.urls import path

from .Views import users, tags, adverts, comments, ratings

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
    path("comment/createComment/<int:advert>", comments.createComment),
    path("comment/tag/<str:tag>", comments.commentsByTag),

    path("rating/user/<int:advert>/<str:user>", ratings.ratingByUserAdvert),
    path("rating/advert/<int:advert>", ratings.ratingOfAdvert),
    path("rating/advert/list/<int:advert>", ratings.advertRatingList),
    path("rating/id/<int:id>", ratings.rating),
    path("rating/createRating/<int:advert>", ratings.createRating),
]