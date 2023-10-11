import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import model_to_dict
from skelbiameAPI.models import Advert, Comment, User, Tag
from .generalFunctions import IsValid, IsFullValid
import datetime

def allComments(request):
    if request.method == "GET":
        data = Comment.objects.all().values("text", "date", "id", "advertid", "user")
        converted = [entry for entry in data]
        return JsonResponse(converted, safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponse(status=405)

def commentsByAdvert(request, advert):
    if request.method == "GET":
        try:
            requestedAdvert = Advert.objects.get(id=advert)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        data = Comment.objects.filter(advertid=advert).values("text", "date", "id", "advertid", "user")
        converted = [entry for entry in data]
        return JsonResponse(converted, safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponse(status=405)

def comment(request, id):
    try:
        requestedComment = Comment.objects.get(id = id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "GET":
        requestedComment = model_to_dict(requestedComment)
        return JsonResponse(requestedComment, safe=False, json_dumps_params={'indent': 2})

    elif request.method == "DELETE":
        requestedComment.delete()
        return HttpResponse()
    elif request.method == "PUT":
        body = json.loads(request.body)

        if len(body) != 0 and IsValid(body, ["text"]):
            requestedComment.text = body["text"]
            try:
                requestedComment.clean_fields()
            except ValidationError:
                return HttpResponse(status=422)
            requestedComment.save()
            return HttpResponse()
    else:
        return HttpResponse(status=405)


def createComment(request):
    if request.method != "POST":
        return HttpResponse(status=405)
    body = json.loads(request.body)
    if IsFullValid(body, ["text", "advertid"]):
        try:
            requestedAdvert = Advert.objects.get(id=body["advertid"])
        except ObjectDoesNotExist:
            return HttpResponse(status=422)
        newComment = Comment()
        newComment.text = body["text"]
        newComment.advertid = requestedAdvert
        newComment.date = datetime.datetime.now()

        requestedUser = User.objects.get(username="admin")
        newComment.user = requestedUser

        try:
            newComment.clean_fields()
        except ValidationError:
            return HttpResponse(status=422)
        newComment.save()
        return HttpResponse(status=201)
    else:
        return HttpResponseBadRequest()

def commentsByTag(request, tag):
    if request.method == "GET":
        try:
            requestedTag = Tag.objects.get(tag=tag)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        adverts = Advert.objects.filter(tag=requestedTag)
        ans = []
        for i in adverts:
            newComments = Comment.objects.filter(advertid=i).values("text", "date", "id", "advertid", "user")
            ans.extend([entry for entry in newComments])
        return JsonResponse(ans, safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponse(status=405)