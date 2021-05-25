import xlrd
from api.models import *
import time

def save_data(data,pid,over):
    success = 0
    fail = 0

    #循环data字典
    for api in data:
        #解析接口信息字典
        name = api.get('接口名称')
        desc = api.get('描述')
        url = api.get('地址')
        method = api.get('方法类型')
        body_type = api.get('参数类型')
        headers = api.get('请求头')
        body = api.get('参数')


        if method == 'POST':
            method = 1
        elif method == 'GET':
            method = 0

        if body_type == 'NONE':
            body_type = 0
        elif body_type == 'URL_ENCODE':
            body_type = 1
        elif body_type == 'JSON':
            body_type = 2

        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if pid not in [None, ''] and name not in [None, ''] and url not in [None, ''] and method not in [None,''] and body_type not in [None, '']:
            #判断pid对应的项目是否存在
            if Project.objects.filter(id=int(pid)).exists():
                #判断接口信息name不存在，直接插库
                if not ApiInfo.objects.filter(name=name).exists():
                    ApiInfo.objects.create(
                        name=name,
                        desc=desc,
                        url=url,
                        method=method,
                        body_type=body_type,
                        headers=headers,
                        body=body,
                        update_time=update_time,
                        project_id=int(pid)
                    )
                    success+=1

                else:
                    #如果接口信息name存在且over==0即跳过此条
                    if over == 0:
                        continue
                    #如果接口信息name存在且over==1即选择覆盖，更新数据库
                    elif over == 1:
                        ApiInfo.objects.filter(name=name).update(
                            name=name,
                            desc=desc,
                            url=url,
                            method=method,
                            body_type=body_type,
                            headers=headers,
                            body=body,
                            update_time=update_time,
                            project_id=int(pid)
                        )
                        success += 1
            else:
                return {"code": 1, "msg": "项目不存在"}
        else:

            fail += 1

    return {"code": 0, "msg": "本次成功导入用例{success}个，导入失败{fail}个".format(
        success=success, fail=fail
    )}


#解析本地excel
def parse_excel(filename,pid,over):
    data=[]
    try:
        book=xlrd.open_workbook('./upload/'+filename)
        sheet=book.sheet_by_index(0)
        #循环每一行，i是行号
        for i in range(1,sheet.nrows):
            dic={}
            #循环每一列，j是列号
            for j in range(0,len(sheet.row_values(i))):
                #把每一行的接口信息组成一个大字典，其中第一行信息固定
                dic[sheet.row_values(0)[j]]=sheet.row_values(i)[j]

            #把接口信息字典存到data列表中
            data.append(dic)

        #调用sava_data解析字典进行插库，并返回成功与失败数
        result=save_data(data,pid,over)
        return result
    except xlrd.biffh.XLRDError:
        return {"code": 1, "msg": "您上传的文件sheet页不存在"}

    except FileNotFoundError:
        return {"code": 1, "msg": "您上传的文件未能正常保存"}