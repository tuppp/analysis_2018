from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the analysis index.")



def averageTemp(request):
    postcode = request.GET.get('postcode',None)
    date = request.GET.get('date',None)
    if postcode==None or date==None:
        return HttpResponse(status=500)
    avgTemp = averageTemp(postcode,date)
    return HttpResponse(avgTemp)
