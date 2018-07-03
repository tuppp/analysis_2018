from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the analysis index.")



def avgMap(request):
    year = request.GET.get('year',2018)
    avgMap = average(year)
    return HttpResponse(avgTemp)


def average(year=2018):
    