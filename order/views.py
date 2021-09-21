from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from order import serializers
from rest_framework.parsers import JSONParser

from order.models import Shop, Menu, Order, OrderFood
from order.serializers import ShopSerializer, MenuSerializer

@csrf_exempt
def shop(request):
    if request.method == "GET":
        # data = Shop.objects.all()
        # serializer = ShopSerializer(data, many=True)
        # return JsonResponse(serializer.data, safe=False)
        data = Shop.objects.all()
        return render(request, "order/shop_list.html",{"shop_list":data})
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ShopSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def menu(request, shop_id):
    if request.method == "GET":
        data = Menu.objects.filter(shop=shop_id)
        # serializer = MenuSerializer(data, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return render(request, "order/menu_list.html", {"menu_list":data, "shop_id":shop_id})

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status=400)

from django.utils import timezone
@csrf_exempt
def order(request):
    if request.method == "POST":
        address = request.POST["address"]
        shop = request.POST["shop"]
        food_list = request.POST.getlist("menu")
        order_date = timezone.now()

        shop_item = Shop.objects.get(pk=int(shop))

        shop_item.order_set.create(address=address, order_date=order_date, shop=int(shop))

        order_item = Order.objects.get(pk = shop_item.order_set.latest('id').id)
        for food in food_list:
            order_item.orderfood_set.create(food_name=food)

        return render(request, "order/success.html")
    elif request.method=="GET":
        order_list = Order.objects.all()
        return render(request, "order/order_list.html", {"order_list":order_list})