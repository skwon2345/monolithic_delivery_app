from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from order.models import Menu, Order, Orderfood, Shop
from order.serializers import MenuSerializer, ShopSerializer
from rest_framework.parsers import JSONParser


@csrf_exempt
def order_list(request):
    if request.method=="GET":
        order_list = Order.objects.all()
        return render(request, "delivery/order_list.html", {"order_list": order_list})

    elif request.method=="POST":
        order_item = Order.objects.get(pk=request.POST["order_id"])
        order_item.deliver_finish = 1
        order_item.save()

        return render(request, "delivery/success.html")