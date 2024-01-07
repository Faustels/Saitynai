from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def tags(request):
    return render(request, "tags.html")

def adverts(request, tag):
    return render(request, "adverts.html")

def advert(request, id):
    return render(request, "advert.html")