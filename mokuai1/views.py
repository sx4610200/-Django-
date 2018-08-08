from django.shortcuts import render
from django.http import HttpResponse
from .models import Users
from .models import Messages
from .models import News
from .models import Office
from django.shortcuts import redirect
import time
import os
from os import path
from django.db import transaction
from django.db.models import F
import qrcode
from django.utils.six import BytesIO
import datetime

def deco(func):
    def _deco(request):
        try:
            loginbean = request.session['loginbean']
            if loginbean == None:
                return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")
            if loginbean['role'] == 0:
                reqFun = func(request, loginbean)
                return reqFun
                # return render(request, 'works/showCreateWorks.html', {'loginbean': loginbean})
            else:
                return HttpResponse("<script>alert('您无权限进入');location.href='/';</script>")
        except Exception as err:
            print(err)
            return HttpResponse("<script>alert('请登录');location.href='/';</script>")

    return _deco


def novel(request):
    print("主页里的session")
    loginbean = None
    try:
        loginbean = request.session['loginbean']
        print(loginbean)
    except Exception as err:
        pass
    return render(request, 'novel.html', {'loginbean': loginbean})


def userhome(request):
    loginbean = request.session["loginbean"]
    print(loginbean['role'])
    print("+++++++++++++++++++++++++++++++++++++++++++")
    if loginbean['role'] ==1or loginbean['role'] ==2:
        print(loginbean['id'])
        rs = Office.objects.filter(uid=loginbean['id']).first()
        return render(request, 'userhome.html', {'loginbean': loginbean, 'rs': rs})
    else:
        return HttpResponse("<script>alert('您无权限进入');location.href='/system/novel/';</script>")


def adminhome(request):
    print('------------进入adminhome方法-----------')
    print(request.session['loginbean'])
    loginbean = request.session['loginbean']
    if loginbean["role"] != 0:
        return HttpResponse("<script>alert('您无权限进入');location.href='/system/novel';</script>")
    else:
        office = Office.objects.filter().all()
        rs = Messages.objects.filter(role=2).all()
        print(rs)
        return render(request, 'iomp/adminhome.html', {'loginbean': loginbean, 'rs': rs, 'office': office})


def loginout(request):
    del request.session['loginbean']
    return redirect('/system/novel')


def loginpanel(request):
    return render(request, 'loginpanel.html')


def zhucepanel(request):
    return render(request, 'zhucepanel.html')


def zhuce(request):
    if request.method == 'POST':
        dict = request.POST.dict()  # 转成字典形式
        print(dict)
        # email = request.POST.get('email')
        # pwd = request.POST.get('pwd')
        # nicheng = request.POST.get('nicheng')
        try:
            del dict['csrfmiddlewaretoken']
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            user = Users.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                        **dict)  # **dict必须放到最后
            print('-------注册里的dict')
            dict['id'] = user.id
            print(dict)
            request.session['login'] = dict
            # return HttpResponse('CG')
            return redirect('/system/login')

        except Exception as err:
            errStr = err.args[1]
            if 'emailuniq' in errStr:
                return HttpResponse("用户名重复")
            elif 'nichenguniq' in errStr:
                return HttpResponse("昵称重复")
            else:
                return HttpResponse("未知错误")
    else:
        return HttpResponse('请正确提交')


def login(request):
    if request.method == 'POST':
        rs = Users.objects.filter(email=request.POST.get('email'), pwd=request.POST.get('pwd')).first()
        if rs != None:
            loginbean = {}
            loginbean['id'] = rs.id
            loginbean['nicheng'] = rs.nicheng
            loginbean['role'] = rs.role
            loginbean['msgnum'] = rs.msgnum
            request.session['loginbean'] = loginbean
            # return redirect("/system/novel")
            if rs.role == 0:
                return redirect('/system/adminhome/')
            elif rs.role == 1 or rs.role == 2:
                return redirect('/system/usershome/')
            elif rs.role == 3:
                return redirect('/system/doctorhome/')
        else:
            return HttpResponse("<script>alert('用户名或密码错误');location.href='/system/novel/';</script>")

    else:

        dict = request.session['login']
        if dict != None:
            loginbean = {}
            loginbean['id'] = dict['id']
            loginbean['nicheng'] = dict['nicheng']
            loginbean['role'] = 1
            request.session['loginbean'] = loginbean
            del request.session['login']
            # return HttpResponse('登录成功')
            return redirect('/system/novel')
        else:
            return HttpResponse('请登录')


def reg(request):
    try:
        # transaction.set_autocommit(False)
        loginbean = request.session['loginbean']
        officename = request.GET.get("test")
        dict = {}
        dict['uid'] = loginbean['id']
        dict['dename'] = loginbean['nicheng']
        dict['officename'] = officename
        officec = Office.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                        **dict)
        # transaction.commit()
        # transaction.set_autocommit(True)
        return HttpResponse("<script>alert('预约成功');location.href='/system/usershome/';</script>")
    except Exception as err:
        print(err)
        # transaction.rollback()
        # transaction.set_autocommit(True)
        return HttpResponse("<script>alert('您今天已进行过预约');location.href='/system/usershome/';</script>")


def createQR(request):
    loginbean = request.session['loginbean']
    uid = loginbean['id']
    office = Office.objects.filter(uid=uid).first()
    r = office.money
    img = qrcode.make('您已缴纳%s元' % r)  # 传入网站计算出二维码图片字节数据
    buf = BytesIO()  # 创建一个BytesIO临时保存生成图片数据
    img.save(buf)  # 将图片字节数据放到BytesIO临时保存
    image_stream = buf.getvalue()  # 在BytesIO临时保存拿出数据
    response = HttpResponse(image_stream, content_type="image/jpg")  # 将二维码数据返回到页面
    return response


def submitmessage(request):
    try:
        loginbean = request.session["loginbean"]
        if loginbean == None:
            return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")
        if request.method != 'POST':
            return render(request, 'novel.html')
        else:
            dict = request.POST.dict()
            print(dict)
            del dict['csrfmiddlewaretoken']
            idperson1 = request.FILES["idperson1"]
            print('---------------2')
            print(idperson1)
            if idperson1 == None:
                return HttpResponse('必须上传身份证照片正面！')
            idperson2 = request.FILES.get("idperson2")
            print(idperson2)
            if idperson2 == None:
                return HttpResponse('必须上传身份证背面！')
            try:
                idimagePath1 = "%s1%s" % (time.time(), idperson1.name)
                f = open(os.path.join("mokuai1\static\imgs", idimagePath1), 'wb')
                for chunk in idperson1.chunks(chunk_size=1024):
                    f.write(chunk)
                dict['idperson1'] = idimagePath1
                idimagePath2 = "%s1%s" % (time.time(), idperson2.name)
                f = open(os.path.join("mokuai1\static\imgs", idimagePath2), 'wb')
                for chunk2 in idperson2.chunks(chunk_size=1024):
                    f.write(chunk2)
                dict['idperson2'] = idimagePath2
                dict['uid'] = loginbean['id']
                print("++++++++++++++++++++++++++++++++")
                print(dict)
                # 入库操作
                message = Messages.objects.create(
                    createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), **dict)
                Users.objects.filter(id=loginbean['id']).update(role=2)
                Users.objects.filter(id=1).update(msgnum=F('msgnum') + 1)
                loginbean['role'] = 2
                request.session['loginbean'] = loginbean
                print(request.session['loginbean'])
                print(message)
            except Exception as e:
                print(e)
            finally:
                f.close()
                return redirect('/system/novel')

    except Exception as err:
        print('--------6')
        print(err)
        return HttpResponse("<script>alert('网页错误');</script>")


def messagespanel(request):
    mid = request.GET.get("mid")
    rs = Messages.objects.filter(id=mid).all()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(rs)
    return render(request, 'iomp/messagespanel.html', {"rs": rs})


def applysuccess(request):
    try:
        transaction.set_autocommit(False)
        uid = request.GET.get("uid")
        print("++++++++++++")
        print(uid)
        loginbean = request.session['loginbean']
        dict = {}
        dict['sendid'] = loginbean['id']
        dict['sendname'] = "管理员"
        dict['contents'] = '申请成功'
        dict['recid'] = uid
        office = Messages.objects.filter(uid=uid).first()
        Users.objects.filter(id=uid).update(role=3, office=office.office, msgnum=F('msgnum') + 1)
        Messages.objects.filter(uid=uid).delete()
        News.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                            **dict)
        transaction.commit()
    except Exception as err:
        print(err)
        transaction.rollback()
    finally:
        transaction.set_autocommit(True)
    return redirect('/system/novel/')


def applyrefuse(request):
    try:
        print('applyrefuse-----')
        transaction.set_autocommit(False)
        loginbean = request.session['loginbean']
        print('检查是否有id传回applyrefuse')
        uid = request.POST.get('receiveid')
        print("++++++++")
        print(uid)
        content = request.POST.get('content')
        dict = {}
        dict['sendid'] = loginbean['id']
        dict['sendname'] = '管理员'
        dict['recid'] = uid
        dict['contents'] = '驳回理由：%s' % (content)
        Users.objects.filter(id=uid).update(role=1, msgnum=F('msgnum') + 1)
        Messages.objects.filter(uid=uid).delete()
        News.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                            **dict)
        transaction.commit()
    except Exception as err:
        print(err)
        transaction.rollback()
    finally:
        transaction.set_autocommit(True)
    return redirect('/system/novel/')


def showImg(request):
    imgurl = request.GET.get('imgurl')
    # 此处的imgurl是前端要显示的地方所写的名字
    print("imgurl")
    print(imgurl)
    d = path.dirname(__file__)
    # print(d)
    imgPath = path.join(d, "static/imgs/" + imgurl)
    # +imgurl：通过路径找到图片在传回前端
    image_data = open(imgPath, "rb").read()
    print('+++++00000')
    return HttpResponse(image_data, content_type="image/png")


def allocation(request):
    officename = request.GET.get("officename")
    offid = request.GET.get("offid")
    print(officename)
    print(offid)
    off = Users.objects.filter(office=officename).all()
    havenuser = Office.objects.filter(officename=officename)
    return render(request, 'iomp/allocationpanel.html', {'off': off, 'havenuser': havenuser, 'offid': offid})


def task(request):
    try:
        # transaction.set_autocommit(False)
        doctorid = request.GET.get("uid")
        OfficeID = request.GET.get("offid")
        doname = request.GET.get("doname")
        print(doctorid)
        print(OfficeID)
        print(doname)
        of = Office.objects.filter(id=OfficeID)
        r = of.first().docid
        # transaction.commit()
        if r != None:
            return HttpResponse("<script>alert('不能重复分配医生');location.href='/system/novel/';</script>")
        else:
            of.update(docid=doctorid, docname=doname)
            Users.objects.filter(id=doctorid).update(sicker=F('sicker') + 1)
            return HttpResponse("<script>alert('成功');location.href='/system/adminhome/';</script>")
    except Exception as err:
        print(err)
        # transaction.rollback()
        # transaction.set_autocommit(True)


def money(request):
    rmb = request.GET.get('rmb')
    uid = request.GET.get('uid')
    Office.objects.filter(uid=uid).update(money=rmb)
    return HttpResponse("<script>alert('通知成功');location.href='/system/adminhome/';</script>")


def doctorhome(request):
    loginbean = request.session["loginbean"]
    docid = loginbean['id']
    rs = Office.objects.filter(docid=docid).all()
    if loginbean['role'] == 3:
        return render(request, 'doctor/doctorhome.html', {'loginbean': loginbean, 'rs': rs})
    else:
        return HttpResponse("<script>alert('您无权限进入');location.href='/system/adminhome/';</script>")

def writeapply (request):
    uid=request.POST.get('uid')
    content=request.POST.get('content')
    Office.objects.filter(uid=uid).update(content=content)
    return HttpResponse("<script>alert('成功');location.href='/system/doctorhome/';</script>")




def writeapplypannel(request):
    uid=request.GET.get('uid')
    print(uid)
    loginbean=request.session['loginbean']
    content = Office.objects.filter(uid=uid)
    return render(request,'doctor/writeapplypannel.html',{'loginbean':loginbean,'uid':uid,'content':content})



def delectusers(request):
    usersid=request.GET.get('usersid')
    users=request.GET.get('users')
    print("+++++++++++++++++++")
    print(users)
    print(usersid)
    Office.objects.filter(id=usersid).delete()
    Users.objects.filter(nicheng=users).update(sicker=F('sicker') - 1)
    return redirect('/system/adminhome/')


def seemessagespanel(request):
    loginbean=request.session['loginbean']
    uid=loginbean['id']
    Users.objects.filter(id=uid).update(msgnum=0)
    news=News.objects.filter(recid=uid)
    return render(request,'seemessagespanel.html',{'loginbean':loginbean,'news':news})


def seemessagesiomppanel(request):
    loginbean=request.session['loginbean']
    print(loginbean)
    Users.objects.filter(id=1).update(msgnum=0)
    return render(request,'iomp/seemessagesiomppanel.html',{'loginbean':loginbean})