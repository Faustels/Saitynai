import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import model_to_dict
from skelbiameAPI.models import User, Rating, Advert
from .generalFunctions import IsValid, IsFullValid

def ratingByUserAdvert(request, advert):
    if request.method == "GET":
        try:
            requestedAdvert = Advert.objects.get(id=advert)
            requestedUser = User.objects.get(username="admin")
            requestedRating = Rating.objects.get(user=requestedUser, advertid=requestedAdvert)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        return JsonResponse(model_to_dict(requestedRating), safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponse(status=405)

def ratingOfAdvert(request, advert):
    if request.method == "GET":
        try:
            requestedAdvert = Advert.objects.get(id=advert)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        requestedRating = Rating.objects.filter(advertid=requestedAdvert)
        ans = 0
        for rating in requestedRating:
            if rating.positive == 1:
                ans += 1
            else:
                ans -= 1
        return JsonResponse({"fullRating": ans}, safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponse(status=405)

def advertRatingList(request, advert):
    if request.method == "GET":
        try:
            requestedAdvert = Advert.objects.get(id=advert)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        requestedRating = Rating.objects.filter(advertid=requestedAdvert)
        ans = []
        for i in requestedRating:
            temp = {"id": i.id, "positive": i.positive == 1, "user": i.user.username, "advertid": i.advertid.id}
            ans.append(temp)

        return JsonResponse(ans, safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponse(status=405)

def rating(request, id):
    try:
        requestedRating = Rating.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "GET":
        requestedRating = model_to_dict(requestedRating)
        return JsonResponse(requestedRating, safe=False, json_dumps_params={'indent': 2})

    elif request.method == "DELETE":
        requestedRating.delete()
        return HttpResponse()

    elif request.method == "PUT":
        body = json.loads(request.body)

        if len(body) != 0 and IsValid(body, ["positive"]):
            if body["positive"] != 1 and body["positive"] != 0:
                return HttpResponse(status=422)
            requestedRating.positive = body["positive"]
            requestedRating.save()
            return HttpResponse()

        else:
            return HttpResponseBadRequest()

    else:
        return HttpResponse(status=405)


def createRating(request, advert):
    if request.method != "POST":
        return HttpResponse(status=405)
    body = json.loads(request.body)
    if IsFullValid(body, ["positive"]):
        try:
            requestedAdvert = Advert.objects.get(id=advert)
        except ObjectDoesNotExist:
            return HttpResponse(status=422)

        requestedUser = User.objects.get(username="admin")

        try:
            requestedRating = Rating.objects.get(user=requestedUser, advertid=requestedAdvert)
        except ObjectDoesNotExist:
            if body["positive"] != 1 and body["positive"] != 0:
                return HttpResponse(status=422)
            newRating = Rating()
            newRating.user = requestedUser

            newRating.positive = body["positive"]
            newRating.advertid = requestedAdvert

            try:
                newRating.clean_fields()
            except ValidationError:
                return HttpResponse(status=422)
            newRating.save()
            return HttpResponse(status=201)

        return HttpResponse(status=409)
    else:
        return HttpResponseBadRequest()