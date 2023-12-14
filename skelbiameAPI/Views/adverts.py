import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import model_to_dict
from skelbiameAPI.models import Advert, Tag, User
from .generalFunctions import IsValid, IsFullValid, EditElement
import datetime
from skelbiameAPI.Tokens import TokenUser, TokenCanEdit, ToPureToken

def allAdverts(request):
    if request.method == "GET":
        data = Advert.objects.all().values("name", "description", "uploadtime", "lastupdatetime", "tag", "id", "user")
        converted = [entry for entry in data]
        return JsonResponse(converted, safe=False, json_dumps_params={'indent': 2})
    elif request.method == "POST":
        return createAdvert(request)
    else:
        return HttpResponse(status=405)
def advert(request, advert):
    try:
        requestedAdvert = Advert.objects.get(id=advert)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "GET":
        requestedAdvert = model_to_dict(requestedAdvert)
        return JsonResponse(requestedAdvert, safe=False, json_dumps_params={'indent': 2})

    token = ToPureToken(request.headers.get("Authorization"))


    if not TokenCanEdit(token, requestedAdvert.user.username):
        return HttpResponseForbidden()

    if request.method == "DELETE":
        requestedAdvert.delete()
        return HttpResponse()

    elif request.method == "PATCH" or request.method == "PUT":
        body = json.loads(request.body)
        isValid = False
        if request.method == "PATCH":
            isValid = IsValid(body, ["name", "description", "tag"])
        else:
            isValid = IsFullValid(body, ["name", "description", "tag"])

        if len(body) != 0 and isValid:
            requestedAdvert.lastupdatetime = datetime.datetime.now()

            EditElement(requestedAdvert, body, ["name", "description"], request.method)
            if "tag" in body:
                try:
                    requestedTag = Tag.objects.get(tag=body["tag"])
                except ObjectDoesNotExist:
                    return HttpResponse(status=422)
                requestedAdvert.tag = requestedTag
            requestedAdvert.tag = requestedTag

            try:
                requestedAdvert.clean_fields()
            except ValidationError:
                return HttpResponse(status=422)
            requestedAdvert.save()
            return JsonResponse(model_to_dict(requestedAdvert), safe=False, json_dumps_params={'indent': 2})
        else:
            return HttpResponseBadRequest()
    else:
        HttpResponse(status=405)

def createAdvert(request):

    token = ToPureToken(request.headers.get("Authorization"))

    username = TokenUser(token)
    if username is None:
        return HttpResponseForbidden()

    body = json.loads(request.body)

    if IsFullValid(body, ["name", "description", "tag"]):
        try:
            requestedTag = Tag.objects.get(tag=body["tag"])
        except ObjectDoesNotExist:
            return HttpResponse(status=422)
        newAdvert = Advert()
        newAdvert.name = body["name"]
        newAdvert.description = body["description"]
        newAdvert.tag = requestedTag
        newAdvert.uploadtime = datetime.datetime.now()

        requestedUser = User.objects.get(username=username)
        newAdvert.user = requestedUser

        try:
            newAdvert.clean_fields()
        except ValidationError:
            return HttpResponse(status=422)
        newAdvert.save()
        return JsonResponse(model_to_dict(newAdvert), status = 201, safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponseBadRequest()

def advertByTag(request, tag):
    if request.method != "GET":
        return HttpResponse(status=405)

    try:
        requestedTag = Tag.objects.get(tag=tag)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    requestedAdverts = Advert.objects.filter(tag=requestedTag).values("name", "description", "uploadtime", "lastupdatetime", "tag", "id", "user")
    converted = [entry for entry in requestedAdverts]
    return JsonResponse(converted, safe=False, json_dumps_params={'indent': 2})



