import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import model_to_dict
from skelbiameAPI.models import Advert, Tag, User
from .generalFunctions import IsValid, IsFullValid
import datetime

def allAdverts(request):
    if request.method == "GET":
        data = Advert.objects.all().values("name", "description", "uploadtime", "lastupdatetime", "tag", "id", "user")
        converted = [entry for entry in data]
        return JsonResponse(converted, safe=False, json_dumps_params={'indent': 2})
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

    elif request.method == "DELETE":
        requestedAdvert.delete()
        return HttpResponse()

    elif request.method == "PUT":
        body = json.loads(request.body)

        if len(body) != 0 and IsValid(body, ["name", "description", "tag"]):
            requestedAdvert.lastupdatetime = datetime.datetime.now()
            if "name" in body:
                requestedAdvert.name = body["name"]
            if "description" in body:
                requestedAdvert.description = body["description"]
            if "tag" in body:
                try:
                    requestedTag = Tag.objects.get(tag=body["tag"])
                except ObjectDoesNotExist:
                    return HttpResponse(status=422)
                requestedAdvert.tag = requestedTag
            try:
                requestedAdvert.clean_fields()
            except ValidationError:
                return HttpResponse(status=422)
            requestedAdvert.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    else:
        HttpResponse(status=405)

def createAdvert(request):
    if request.method != "POST":
        return HttpResponse(status=405)
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

        requestedUser = User.objects.get(username="admin")
        newAdvert.user = requestedUser

        try:
            newAdvert.clean_fields()
        except ValidationError:
            return HttpResponse(status=422)
        newAdvert.save()
        return HttpResponse(status=201)
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



