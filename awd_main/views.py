# from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from dataentry.tasks import celery_test_task


def home(request):
    # return HttpResponse("<h1>Home</h1>")
    return render(request, "home.html")


def celery_test(request):
    # I want to execute a time consuming task here
    result = celery_test_task.delay()
    return HttpResponse(f"<h3>Function executed successfully!</h3>")