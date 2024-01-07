import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import model_to_dict
from skelbiameAPI.models import User, Rating, Advert
from .generalFunctions import IsValid, IsFullValid
from skelbiameAPI.Tokens import TokenIsAdmin, TokenUser, TokenCanEdit, ToPureToken

def ratingByUserAdvert(request, advert):
    token = ToPureToken(request.headers.get("Authorization"))

    username = TokenUser(token)
    if username is None:
        return HttpResponseForbidden()

    if request.method == "GET":
        try:
            requestedAdvert = Advert.objects.get(id=advert)
            requestedUser = User.objects.get(username=username)
            requestedRating = Rating.objects.get(user=requestedUser, advertid=requestedAdvert)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        return JsonResponse(model_to_dict(requestedRating), safe=False, json_dumps_params={'indent': 2})
    elif request.method == "POST" or request.method == "PATCH" or request.method == "PUT" or request.method == "DELETE":
        return createRating(request, advert)
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

        userRating = None

        token = ToPureToken(request.headers.get("Authorization"))
        username = TokenUser(token)
        if username is not None:
            try:
                requestedUser = User.objects.get(username=username)
                requestedRating = Rating.objects.get(user=requestedUser, advertid=requestedAdvert)
                userRating = requestedRating.positive == 1
            except:
                pass
        return JsonResponse({"fullRating": ans, "userPositive": userRating}, safe=False, json_dumps_params={'indent': 2})
    elif request.method == "POST" or request.method == "PATCH" or request.method == "PUT" or request.method == "DELETE":
        return createRating(request, advert)
    else:
        return HttpResponse(status=405)

def advertRatingList(request, advert):
    token = ToPureToken(request.headers.get("Authorization"))

    if not TokenIsAdmin(token):
        return HttpResponseForbidden()

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
    token = ToPureToken(request.headers.get("Authorization"))

    try:
        requestedRating = Rating.objects.get(id=id)
    except ObjectDoesNotExist:
        if not TokenIsAdmin(token):
            return HttpResponseForbidden()
        return HttpResponseNotFound()

    if not TokenCanEdit(token, requestedRating.user.username):
        return HttpResponseForbidden()

    if request.method == "GET":
        requestedRating = model_to_dict(requestedRating)
        return JsonResponse(requestedRating, safe=False, json_dumps_params={'indent': 2})

    else:
        return HttpResponse(status=405)


def createRating(request, advert):
    token = ToPureToken(request.headers.get("Authorization"))

    username = TokenUser(token)
    if username is None:
        return HttpResponseForbidden()

    requestedUser = User.objects.get(username=username)

    if request.method == "PUT" or request.method == "PATCH":
        body = json.loads(request.body)
        if len(body) != 0 and IsValid(body, ["positive"]):
            if body["positive"] != 1 and body["positive"] != 0:
                return HttpResponse(status=422)
            try:
                requestedRating = Rating.objects.get(advertId=advert, user= requestedUser)
                requestedRating.positive = body["positive"]
                requestedRating.save()
                return HttpResponse()
            except:
                return HttpResponseNotFound()

        else:
            return HttpResponseBadRequest()

    if request.method == "DELETE":
        try:
            requestedRating = Rating.objects.get(advertId=advert, user=requestedUser)
            requestedRating.delete()
            return HttpResponse()
        except:
            return HttpResponseNotFound()
    elif request.method == "POST":
        body = json.loads(request.body)
        if IsFullValid(body, ["positive"]):
            try:
                requestedAdvert = Advert.objects.get(id=advert)
            except ObjectDoesNotExist:
                return HttpResponse(status=422)

            try:
                requestedRating = Rating.objects.get(user=requestedUser, advertid=requestedAdvert)
                return HttpResponse(status=409)
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
