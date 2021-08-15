# -*- coding: utf-8 -*-
from .models import GoodsInfo,TypeInfo
from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
# Query the latest 4 items of each category and the 4 items with the highest click-through rate
def index(request):
    """
    The index function is responsible for querying the content of the product that needs to be displayed on the page,
    Mainly the 4 latest products in each category and the 4 products with the highest click-through rate.
    Each type of commodity needs to be inquired twice
    """
    count = request.session.get('count')
    fruit = GoodsInfo.objects.filter(gtype__id=2).order_by("-id")[:4]
    fruit2 = GoodsInfo.objects.filter(gtype__id=2).order_by("-gclick")[:4]
    fish = GoodsInfo.objects.filter(gtype__id=4).order_by("-id")[:4]
    fish2 = GoodsInfo.objects.filter(gtype__id=4).order_by("-gclick")[:3]
    meat = GoodsInfo.objects.filter(gtype__id=1).order_by("-id")[:4]
    meat2 = GoodsInfo.objects.filter(gtype__id=1).order_by("-gclick")[:4]
    egg = GoodsInfo.objects.filter(gtype__id=5).order_by("-id")[:4]
    egg2 = GoodsInfo.objects.filter(gtype__id=5).order_by("-gclick")[:4]
    vegetables = GoodsInfo.objects.filter(gtype__id=3).order_by("-id")[:4]
    vegetables2 = GoodsInfo.objects.filter(gtype__id=3).order_by("-gclick")[:4]
    frozen = GoodsInfo.objects.filter(gtype__id=6).order_by("-id")[:4]
    frozen2 = GoodsInfo.objects.filter(gtype__id=6).order_by("-gclick")[:4]
    # count = CartInfo.objects.filter(
    #     user_id=request.session.get('userid')).count()   'count':count,
    # # Constructing the context
    context = {'title':'Home','fruit': fruit,
               'fish': fish,'meat': meat,'egg': egg,
               'vegetables': vegetables,'frozen': frozen,
               'fruit2': fruit2,'fish2': fish2,'meat2': meat2,
               'egg2': egg2,'vegetables2': vegetables2,'frozen2': frozen2,
               'guest_cart': 1,'page_name':0,'count':count}

    # Return to the rendering template
    return render(request, 'df_goods/index.html', context)


#Product List
def goodlist(request, typeid, pageid, sort):
    """
    The goodlist function is responsible for displaying information about a certain type of commodity.
    The parameters in the url in turn represent
    typeid: product type id; selectid: query condition id, 1 is to query based on id, 2 to query based on price, and 3 to query based on click volume
    """
    count = request.session.get('count')
    # Get the latest products
    newgood = GoodsInfo.objects.all().order_by('-id')[:2]
    # Query all products based on conditions
    if sort == '1':#according to the latest gtype_id, gtype__id refers to typeinfo_id
        sumGoodList = GoodsInfo.objects.filter(
            gtype_id=typeid).order_by('-id')
    elif sort == '2':#by price
        sumGoodList = GoodsInfo.objects.filter(
            gtype__id=typeid).order_by('gprice')
    elif sort == '3':#according to the number of clicks
        sumGoodList = GoodsInfo.objects.filter(
            gtype__id=typeid).order_by('-gclick')
    # Paging
    paginator = Paginator(sumGoodList, 15)
    goodList = paginator.page(int(pageid))
    pindexlist = paginator.page_range
    # print pindexlist xrange(1,2)
    # Determine the type of product
    goodtype = TypeInfo.objects.get(id=typeid)
    # count = CartInfo.objects.filter(
    #     user_id=request.session.get('userid')).count()
    # Construct context'count': count,
    context = {'title':'Product details','list': 1,
               'guest_cart': 1,'goodtype': goodtype,
               'newgood': newgood,'goodList': goodList,
               'typeid': typeid,'sort': sort,
               'pindexlist': pindexlist,'pageid': int(pageid),'count':count}

    # Render the return result
    return render(request, 'df_goods/list.html', context)


def detail(request,id):
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick=goods.gclick+1
    goods.save()
    # Query the current commodity type goodsinfo__id value
    # goodtype = TypeInfo.objects.get(goodsinfo__id=id)
    goodtype = goods.gtype
    # type = TypeInfo()

    count = request.session.get('count')
    #goods.gtype = typeinfo goods.gtype.goodsinfo_set -> typeinfo.goodsinfo_set
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    # print'*' * 10
    # print news[0].gtitle
    # print goodtype pork, beef and mutton
    # print goods.gtype Pork, Beef and Mutton

    context={'title':goods.gtype.ttitle,'guest_cart':1,
             'g':goods,'newgood':news,'id':id,
             'isDetail': True,'list':1,'goodtype': goodtype,'count':count}
    response=render(request,'df_goods/detail.html',context)


    #Use cookies to record recently viewed product id

    #Get cookies
    goods_ids = request.COOKIES.get('goods_ids','')
    #Get current click product id
    goods_id='%d'%goods.id
    #Determine whether the product id in cookies is empty
    if goods_ids!='':
        #Split out each product id
        goods_id_list=goods_ids.split(',')
        #Determine whether the product already exists in the list
        if goods_id_list.count(goods_id)>=1:
            #Remove if it exists
            goods_id_list.remove(goods_id)
        #Add in the first place
        goods_id_list.insert(0, goods_id)
        #Judging whether the number of lists exceeds 5
        if len(goods_id_list)>=6:
            #If more than five, delete the sixth
            del goods_id_list[5]
        #Add product id to cookies
        goods_ids=','.join(goods_id_list)
    else:
        #Add for the first time, add directly
        goods_ids=goods_id
    response.set_cookie('goods_ids',goods_ids)

    return response