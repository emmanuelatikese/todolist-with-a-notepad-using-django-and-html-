from django.shortcuts import render
from django.http import HttpResponse


def mainHome(request):
    return HttpResponse('hi')
