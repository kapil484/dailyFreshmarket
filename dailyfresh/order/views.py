from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.db import transaction
from datetime import datetime
from decimal import Decimal
from .models import OrderInfo,OrderDetailInfo
from user.islogin import islogin
from cart.models import CartInfo
from goods.models import GoodsInfo
from user.models import UserInfo
from django.http import JsonResponse


# Create your views here.
@islogin
def order(request):
    """
    This function user displays data to the order page
    Receive the id of the item in the shopping cart sent by the GET method on the shopping cart page, and construct the shopping cart object for order use
    """

    uid = request.session.get('user_id')
    user = UserInfo.objects.get(id=uid)

    # Get each selected order object, construct it into a list, and pass it to the order page as a context
    orderid = request.GET.getlist('orderid')
    orderlist = []

    for id in orderid:
        orderlist.append(CartInfo.objects.get(id=int(id)))

    # Determine whether the user's mobile phone number is empty, and display them separately
    if user.uphone =='':
        uphone =''
    else:
        uphone = user.uphone[0:4] + \
            '****' + user.uphone[-4:]

    # Construct context
    context = {'title':'Submit order','page_name': 1,'orderlist': orderlist,
               'user': user, 'ureceive_phone': uphone}

    return render(request, 'df_order/place_order.html', context)


#--------------------------------------------What decorator? ->Transaction Once one operation fails, all operations will be rolled back
@transaction.atomic()
@islogin
def order_handle(request):
    #Save a thing point
    tran_id = transaction.savepoint()
    #Receive shopping cart number
    # Get information based on POST and session
    # cart_ids=post.get('cart_ids')
    try:
        post = request.POST
        orderlist = post.getlist('id[]')
        total = post.get('total')
        address = post.get('address')

        order=OrderInfo()
        now=datetime.now()
        uid = request.session.get('user_id')
        order.oid='%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id=uid
        order.odate=now
        order.ototal=Decimal(total)
        order.oaddress = address
        order.save()

        # Traverse the submitted information in the shopping cart and create an order detail table
        for orderid in orderlist:
            cartinfo = CartInfo.objects.get(id=orderid)
            # good = GoodsInfo.objects.get(cartinfo__id=cartinfo.id)
            good = GoodsInfo.objects.get(pk=cartinfo.goods_id)
            # print'*'*10
            # print cartinfo.goods_id
            # Determine whether the inventory is sufficient
            if int(good.gkucun) >= int(cartinfo.count):
                # Inventory is enough, remove the purchased quantity and save
                good.gkucun -= int(cartinfo.count)
                good.save()

                goodinfo = GoodsInfo.objects.get(cartinfo__id=orderid)

                # Create order details table
                detailinfo = OrderDetailInfo()
                detailinfo.goods_id = int(goodinfo.id)
                detailinfo.order_id = int(order.oid)
                detailinfo.price = Decimal(int(goodinfo.gprice))
                detailinfo.count = int(cartinfo.count)
                detailinfo.save()

                # Cyclically delete shopping cart objects
                cartinfo.delete()
            else:
                # Insufficient inventory to start the transaction rollback
                transaction.savepoint_rollback(tran_id)
                # Return json for the front desk to prompt failure
                return JsonResponse({'status': 2})
    except Exception as e:
            #print'==================%s'%e
            transaction.savepoint_rollback(tran_id)
        # Return json for the front desk to prompt success
    return JsonResponse({'status': 1})

        #
    # cart_ids1=[int(item) for item in cart_ids.split(',')]
    # for id1 in cart_ids1:
    # detail=OrderDetailInfo()
    # detail.order=order
    # #Query shopping cart information
    # cart=CartInfo.objects.get(id=id1)
    # #Judging product inventory
    # goods=cart.goods
    # if goods.gkuncun>=cart.count:
    # #Reduce product inventory
    # goods.gkuncun=cart.goods.gkuncun-cart.count
    # goods.save()
    # #Improve order information
    # detail.goods_id=goods.id
    # detail.price=goods.gprice
    # detail.count=cart.count
    # detail.save()
    # #Delete shopping cart data
    # cart.delete()
    # else:
    # transaction.savepoint_rollback(tran_id)
    # return redirect('/cart/')
    # #return HttpResponse
    # transaction.savepoint_commit(tran_id)
    # except Exception as e:
    # print'==================%s'%e
    # transaction.savepoint_rollback(tran_id)
    #
    # return redirect('/user/order/')




# @transaction.atomic()
def pay(request,oid):
    tran_id = transaction.savepoint()
    # try:
    order = OrderInfo.objects.get(oid=oid)
    order.zhifu = 1

    order.save()
    # except Exception as e:
    # print '==================%s' % e
    # transaction.savepoint_rollback(tran_id)
    #print '*' * 10
    #print order.zhifu
    #print order.oid
    context = {'oid': oid}
    return render(request, 'df_order/pay.html', context)
