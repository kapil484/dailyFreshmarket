from hashlib import sha1
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from .models import UserInfo
from .islogin import islogin

# Create your views here.

def register(request):
    return render(request,'user/register.html')

def register_handle(requst):
    response = HttpResponse()
    # Receive user input
    post = requst.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')

    if upwd != ucpwd:
        return redirect('/user/register/')
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()

    return redirect('/user/login/')

def register_exist(requset):
    uname = requset.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})

def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': 'User login', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'user/login.html', context)

def login_handle(request):
    # Receive request information
    get = request.POST
    uname = get.get('username')
    upwd = get.get('pwd')
    jizhu = get.get('jizhu', 0)
    # Query object based on user name
    users = UserInfo.objects.filter(uname=uname)
    # print uname
    # Judge if the user name is not found, then the user name is wrong, if found, then judge whether the password is correct, then go to the user center
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        #Login with cookie value must be red = HttpResponseRedirect red.set_cookie renturn red
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/info')
            count = CartInfo.objects.filter(user_id=users[0].id).count()

            # print'*'*10
            # print count
            # Remember Account Name
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            request.session['count'] = count
            return red
        else:
            context = {'title':'User login','error_name': 0,'error_pwd': 1,'uname': uname}
            return render(request,'df_user/login.html', context)
    else:
        context = {'title':'User login','error_name': 1,'error_pwd': 0,'uname': uname}
        return render(request,'df_user/login.html', context)


# Login User Center
@islogin
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail

    #Recently Viewed
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id_list = goods_ids.split(',')
    goods_list=[]
    if len(goods_ids):
        for goods_id in goods_id_list:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title': '用户中心',
               'user_email': user_email,
               'user_name': request.session['user_name'],
               'page_name':1,'info':1,
               'goods_list':goods_list}
    return render(request, 'df_user/user_center_info.html', context)


# Order
@islogin
def order(request):
    context = {'title':'User Center','page_name':1,'order':1}
    return render(request,'df_user/user_center_order.html', context)


# Shipping address
@islogin
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method =='POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uphone = post.get('uphone')
        user.uyoubian = post.get('uyoubian')
        user.save()
    context = {'title':'User Center','user': user,'page_name':1,'site':1}
    return render(request,'df_user/user_center_site.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


@islogin
def user_center_order(request, pageid):
    """
    The user on this page displays the order submitted by the user, which is transferred from the shopping cart page after the order is placed, or can be viewed from the personal information page
    Sort according to whether the user's order is paid or not, and the order is placed
    """

    uid = request.session.get('user_id')
    # Order information, sorted according to whether to pay and order
    orderinfos = OrderInfo.objects.filter(
        user_id=uid).order_by('zhifu','-oid')

    # Paging
    #Get the orderinfos list with two as one page list
    paginator = Paginator(orderinfos, 2)
    # Get the pageid value of the above collection
    orderlist = paginator.page(int(pageid))
    #Get how many pages in total
    plist = paginator.page_range
    #3page pagination display
    qian1 = 0
    hou = 0
    hou2 = 0
    qian2 = 0
    # dd = dangqian ye
    dd = int(pageid)
    lenn = len(plist)
    if dd>1:
        qian1 = dd-1
    if dd>=3:
        qian2 = dd-2
    if dd<lenn:
        hou = dd+1
    if dd+2<=lenn:
        hou2 = dd+2



    # Construct context
    context = {'page_name': 1,'title':'All orders','pageid': int(pageid),
               'order': 1,'orderlist': orderlist,'plist': plist,
               'pre':qian1,'next':hou,'pree':qian2,'lenn':lenn,'nextt':hou2}

    return render(request, 'df_user/user_center_order.html', context)

