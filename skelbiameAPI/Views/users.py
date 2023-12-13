import json
from hashlib import sha256
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import model_to_dict
from skelbiameAPI.models import User, Role
from .generalFunctions import IsValid, IsFullValid
from skelbiameAPI.Tokens import TokenUser, TokenCanEdit, ToPureToken

def CreatePassword(password):
    return sha256(password.encode("utf-8")).hexdigest()
def users(request):
    if request.method == "GET":
        data = User.objects.all().values("username", "email", "role")
        converted = [entry for entry in data]
        return JsonResponse(converted, safe=False, json_dumps_params={'indent': 2})
    elif request.method == "POST":
        return createUser(request)
    else:
        return HttpResponse(status=405)

def user(request, name):
    try:
        requestedUser = User.objects.get(username = name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "GET":
        requestedUser = model_to_dict(requestedUser)
        del requestedUser["password"]
        del requestedUser["last_login"]
        return JsonResponse(requestedUser, safe=False, json_dumps_params={'indent': 2})

    token = ToPureToken(request.headers.get("Authorization"))

    if not TokenCanEdit(token, requestedUser.username):
        return HttpResponseForbidden()

    if request.method == "DELETE":
        requestedUser.delete()
        return HttpResponse()

    elif request.method == "POST":
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
                newUser.role = Role.objects.get(role="user")

                try:
                    newUser.clean_fields()
                except ValidationError:
                    return HttpResponse(status=422)
                newUser.save()
                return HttpResponse(status=201)
        else:
            return HttpResponseBadRequest()

    elif request.method == "PATCH" or request.method == "PUT":
        body = json.loads(request.body)
        isValid = False
        if request.method == "PATCH":
            isValid = IsValid(body, ["email", "password"])
        else:
            isValid = IsFullValid(body, ["email", "password"])
        if len(body) != 0 and isValid:
            if "email" in body:
                requestedUser.email = body["email"]
            if "password" in body:
                requestedUser.password = CreatePassword(body["password"])
            try:
                requestedUser.clean_fields()
            except ValidationError:
                return HttpResponse(status=422)
            requestedUser.save()
            tempuser = model_to_dict(requestedUser)
            del tempuser["password"]
            del tempuser["last_login"]
            return JsonResponse(tempuser, safe=False, json_dumps_params={'indent': 2})

        else:
            return HttpResponseBadRequest()

    else:
        return HttpResponse(status=405)


def createUser(request):
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
            newUser.role = Role.objects.get(role="user")

            try:
                newUser.clean_fields()
            except ValidationError:
                return HttpResponse(status=422)
            newUser.save()
            return JsonResponse(model_to_dict(newUser), status = 201, safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponseBadRequest()