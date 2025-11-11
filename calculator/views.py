from django.shortcuts import render
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("hello world im shreyas")

def calculator(request):
    return render(request, 'calculator/calculator.html')
