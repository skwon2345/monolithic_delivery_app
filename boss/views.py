from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from order.models import Menu, Order, Orderfood, Shop
from order.serializers import MenuSerializer, ShopSerializer
from rest_framework.parsers import JSONParser


@csrf_exempt
def order_list(request, shop):
    if request.method=="GET":
        order_list = Order.objects.filter(shop=shop)
        return render(request, "boss/order_list.html", {"order_list": order_list})
    else:
        return HttpResponse(status=404)

@csrf_exempt
def time_input(request):
    if request.method=="POST":
        order_item = Order.objects.get(pk=request.POST["order_id"])
        shop = order_item.shop.id
        order_item.estimated_time = request.POST["estimated_time"]
        order_item.save()

        return render(request, "boss/success.html", {"shop": shop})
    else:
        return HttpResponse(status=404)
