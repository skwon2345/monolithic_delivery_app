from rest_framework import serializers

from .models import Menu, Order, Orderfood, Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"
