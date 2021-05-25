from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from .models import *

def home(request):
    return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')

def signout(request):
    request.session['user'] = None
    return HttpResponseRedirect('/login/')

def login(request):
    return render(request, 'login.html')

def check_username(request):
    name = request.POST.get('name')
    if name:
        users = User.objects.filter(name=name)
        if users.exists():
            return JsonResponse({"valid": False})
    return JsonResponse({"valid": True})

def signup_submit(request):
    name = request.POST.get('username', None)
    password = request.POST.get('password', None)
    email = request.POST.get('email', None)
    if name and password and email:
        users = User.objects.filter(name=name)
        if not users.exists():
            try:
                User.objects.create(name=name, password=password, email=email)
                return render(request, 'alert.html',
                              {'data': json.dumps({'url': '/login/', 'flag': 0, 'message': u'注册成功'})})
            except:
                return render(request, 'alert.html',
                              {'data': json.dumps({'url': '/signup/', 'flag': 1, 'message': u'信息存储错误'})})
        else:
            return render(request, 'alert.html', {'data': json.dumps({'url': '/signup/', 'flag': 1, 'message': u'用户名重复'})})
    else:
        return render(request, 'alert.html', {'data': json.dumps({'url': '/signup/', 'flag': 1, 'message': u'缺少必填项'})})

def login_submit(request):
    name = request.POST.get('username', None)
    password = request.POST.get('password', None)
    print(password)
    if name and password:
        users = User.objects.filter(name=name, password=password)
        if users.exists():
            request.session['user'] = users.first().name
            request.session.set_expiry(0)
            return HttpResponseRedirect('/home/')
        else:
            return render(request, 'alert.html',
                          {'data': json.dumps({'url': '/login/', 'flag': 1, 'message': u'用户名或密码错误'})})
    return render(request, 'alert.html', {'data': json.dumps({'url': '/login/', 'flag': 1, 'message': u'登录失败'})})