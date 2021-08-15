# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from user.islogin import islogin
from .models import *
from django.http import JsonResponse

# Create your views here....
#shopping cart
@islogin
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    lenn = len(carts)
    context={'title':'shopping cart',
             'page_name':1,
             'carts':carts,
             'len':lenn}
    return render(request,'cart/cart.html',context)

#Adding goods
@islogin
def add(request,gid,count):
    #User uid purchased gid goods, the quantity is count
    uid=request.session['user_id']
    gid = int(gid)
    count = int(count)
    #Query whether the shopping cart already has this product, add it if there is
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts)>=1:
        cart=carts[0]
        # print'*'*10
        # print cart -> the number of items in the shopping cart
        cart.count=cart.count+count
    else: #If it doesn't exist, add it directly
        cart=CartInfo()
        cart.user_id=uid
        cart.goods_id=gid
        cart.count=count
    cart.save()
    count_s = CartInfo.objects.filter(user_id=uid).count()
    request.session['count'] = count_s
    #If it is an ajax request, return json, otherwise turn to the shopping cart
    if request.is_ajax():
        # count=CartInfo.objects.filter(user_id=request.session['user_id']).count()

        #print'*'*10
        #print'ajax'
        #--------------Unused
        return JsonResponse({'count':count_s})
    else:
        return redirect('/cart/')

@islogin
def edit(request,cart_id,count):
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        count1=cart.count=int(count)
        cart.save()
        data={'ok':0}
    except Exception as e:
        data={'ok':count1}
    return JsonResponse(data)

@islogin
def delete(request,cart_id):

    # try:
    cart = CartInfo.objects.get(pk=int(cart_id))
    cart.delete()
    # print '*'*10
    # print ('delete')
    # data={'ok':1}
    # except Exception as e:
    count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
    request.session['count'] = count
    data={'count':count}
    # print '*' * 10
    # print (count)
    return JsonResponse(data)