import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from skelbiameAPI.models import Tag
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .generalFunctions import IsFullValid
from skelbiameAPI.Tokens import TokenIsAdmin, ToPureToken
from django.forms.models import model_to_dict


def tags(request):
    if request.method == "GET":
        data = Tag.objects.all().values("tag")
        converted = [entry for entry in data]
        return JsonResponse(converted, safe=False, json_dumps_params={'indent': 2})
    elif request.method == "POST":
        return createTag(request)
    else:
        return HttpResponse(status=405)


def tag(request, name):
    try:
        requestedTag = Tag.objects.get(tag=name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "DELETE":
        token = ToPureToken(request.headers.get("Authorization"))

        if not TokenIsAdmin(token):
            return HttpResponseForbidden()

        requestedTag.delete()
        return HttpResponse()
    else:
        return HttpResponse(status=405)


def createTag(request):
    token = ToPureToken(request.headers.get("Authorization"))

    if not TokenIsAdmin(token):
        return HttpResponseForbidden()

    body = json.loads(request.body)

    if IsFullValid(body, ["tag"]):
        try:
            requestedTag = Tag.objects.get(tag=body["tag"])
            return HttpResponse(status=409)
        except ObjectDoesNotExist:
            newTag = Tag()
            newTag.tag = body["tag"]

            try:
                newTag.clean_fields()
            except ValidationError:
                return HttpResponse(status=422)
            newTag.save()
            return JsonResponse(model_to_dict(newTag), status=201, safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponseBadRequest()
