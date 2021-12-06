from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import User
from .serializers import UserSerializer


@csrf_exempt
def user(request):
    if request.method == "GET":
        user = User.objects.all()
        return render(request, "user/user_list.html", {"user_list": user})

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def login(request):
    if request.method == "POST":
        name = request.POST["name"]
        try:
            request.session["user_id"] = User.objects.get(name=name).id

            return render(request, "user/success.html")
        except Exception as e:
            print(e)
            return render(request, "user/fail.html")

    elif request.method == "GET":
        return render(request, "user/login.html")

