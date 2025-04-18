from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello World")

def demo(request):
    return HttpResponse("Demo Page")
def demo2(request):
    return HttpResponse("Demo Page 2")
def nothing(request):
    return HttpResponse("Nothing")

