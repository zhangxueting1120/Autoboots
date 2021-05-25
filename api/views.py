#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from api.models import *
import time
import json
from api.util import *
from api.HttpClient import *
import traceback
import sys
sys.getdefaultencoding()



#项目管理页
def project(request):
    projects = Project.objects.all()
    return render(request,'project.html',{"projects":projects})


#项目编辑接口
def project_update(request):
    pid = request.POST.get('pid')
    name=request.POST.get('title')
    desc=request.POST.get('desc')
    print(pid,name,desc)

    if pid not in ['',None] and name not in ['',None] and desc not in ['',None]:
        if len(name) <= 10 and len(desc)<=30:

            if not Project.objects.filter(name=name).exists() or Project.objects.filter(id=int(pid)).first().name==name:
                try:
                    query=Project.objects.filter(id=int(pid)).first()
                    query.name=name
                    query.desc = desc
                    query.save()

                    return JsonResponse({"code": 0, "msg": "项目更新成功"})
                except Exception as e:
                    print(e)
                    return JsonResponse({"code": 1, "msg": "数据库错误"})
            else:
                return JsonResponse({"code": 1, "msg": "需求名称重复"})

        else:
            return JsonResponse({"code": 1, "msg": "需求名称或描述过长"})
    else:
        return JsonResponse({"code": 1, "msg": "缺少必填参数"})


#项目删除接口
def project_delete(request):

    pid = request.POST.get('pid')
    print(pid)

    if pid:
        try:
            pid = int(pid)
        except Exception as e:
            print(e)
            return JsonResponse({"code": 1, "msg": "参数类型错误"})

        query=Project.objects.filter(id=pid)
        if query.exists():
            query.delete()

            return JsonResponse({"code":0,"msg":"删除成功"})
        else:
            return JsonResponse({"code": 1, "msg": "需求不存在"})
    else:
        return JsonResponse({"code": 1, "msg": "缺少pid"})


#项目新增接口
def project_add(request):
    name = request.POST.get('title')
    desc = request.POST.get('desc')

    if name is not ['',None] and desc is not ['',None]:
        if len(name)<=10 and len(desc) <=30:
            try:
                Project.objects.create(name=name,desc=desc)

                return HttpResponseRedirect('/api/project/')
            except Exception as e:
                print(e)
                return HttpResponse("数据库错误")

        else:
            return HttpResponse("需求名称或描述过长")
    else:
        return HttpResponse("缺少必填参数")

