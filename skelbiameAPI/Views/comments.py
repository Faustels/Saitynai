import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import model_to_dict
from skelbiameAPI.models import Advert, Comment, User, Tag
from .generalFunctions import IsValid, IsFullValid
import datetime
from skelbiameAPI.Tokens import TokenCanEdit, TokenUser, ToPureToken

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
    elif request.method == "POST":
        return createComment(request, advert)
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

    token = ToPureToken(request.headers.get("Authorization"))

    if not TokenCanEdit(token, requestedComment.user.username):
        return HttpResponseForbidden()

    if request.method == "DELETE":
        requestedComment.delete()
        return HttpResponse()
    elif request.method == "PUT" or request.method == "PATCH":
        body = json.loads(request.body)
        if len(body) != 0 and IsValid(body, ["text"]):
            requestedComment.text = body["text"]
            try:
                requestedComment.clean_fields()
            except ValidationError:
                return HttpResponse(status=422)
            requestedComment.save()
            return JsonResponse(model_to_dict(requestedComment), status=200, safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponse(status=405)


def createComment(request, advert):
    token = ToPureToken(request.headers.get("Authorization"))

    username = TokenUser(token)
    if username is None:
        return HttpResponseForbidden()

    body = json.loads(request.body)
    if IsFullValid(body, ["text"]):
        try:
            requestedAdvert = Advert.objects.get(id=advert)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        newComment = Comment()
        newComment.text = body["text"]
        newComment.advertid = requestedAdvert
        newComment.date = datetime.datetime.now()

        requestedUser = User.objects.get(username=username)
        newComment.user = requestedUser

        try:
            newComment.clean_fields()
        except ValidationError:
            return HttpResponse(status=422)
        newComment.save()
        return JsonResponse(model_to_dict(newComment), status=201, safe=False, json_dumps_params={'indent': 2})
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