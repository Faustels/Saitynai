import json
from hashlib import sha256
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import model_to_dict
from skelbiameAPI.models import User
from .generalFunctions import IsValid, IsFullValid

def CreatePassword(password):
    return sha256(password.encode("utf-8")).hexdigest()
def users(request):
    if request.method == "GET":
        data = User.objects.all().values("username", "email")
        converted = [entry for entry in data]
        return JsonResponse(converted, safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponseBadRequest()

def user(request, name):
    try:
        requestedUser = User.objects.get(username = name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "GET":
        requestedUser = model_to_dict(requestedUser)
        del requestedUser["password"]
        return JsonResponse(requestedUser, safe=False, json_dumps_params={'indent': 2})

    elif request.method == "DELETE":
        requestedUser.delete()
        return HttpResponse()

    elif request.method == "PUT":
        body = json.loads(request.body)

        if len(body) != 0 and IsValid(body, ["email", "password"]):
            if "email" in body:
                requestedUser.email = body["email"]
            if "password" in body:
                requestedUser.password = CreatePassword(body["password"])
            try:
                requestedUser.clean_fields()
            except ValidationError:
                return HttpResponse(status=422)
            requestedUser.save()
            return HttpResponse()

        else:
            return HttpResponseBadRequest()

    else:
        return HttpResponseBadRequest()


def createUser(request):
    if request.method != "POST":
        return HttpResponseBadRequest()
    body = json.loads(request.body)
    if IsFullValid(body, ["username", "email", "password"]):
        try:
            requestedUser = User.objects.get(username=body["username"])
            return HttpResponse(status=409)
        except ObjectDoesNotExist:
            newUser = User()
            newUser.username = body["username"]
            newUser.email = body["email"]
            newUser.password = CreatePassword(body["password"])

            try:
                newUser.clean_fields()
            except ValidationError:
                return HttpResponse(status=422)
            newUser.save()
            return HttpResponse(status=201)
    else:
        return HttpResponseBadRequest()