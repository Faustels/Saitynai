import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from skelbiameAPI.models import Tag
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .generalFunctions import IsFullValid


def tags(request):
    if request.method == "GET":
        data = Tag.objects.all().values("tag")
        converted = [entry for entry in data]
        return JsonResponse(converted, safe=False, json_dumps_params={'indent': 2})
    else:
        return HttpResponse(status=405)


def tag(request, name):
    try:
        requestedTag = Tag.objects.get(tag=name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "DELETE":
        requestedTag.delete()
        return HttpResponse()
    else:
        return HttpResponse(status=405)


def createTag(request):
    if request.method != "POST":
        return HttpResponse(status=405)
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
            return HttpResponse(status=201)
    else:
        return HttpResponseBadRequest()
