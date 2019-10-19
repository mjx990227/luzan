import math
import os
import re

from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from server import  models
from common import returnResult
from luzan1 import settings
from datetime import datetime, timezone
from django.forms import forms
from DjangoUeditor.forms import UEditorField
class TestUEditorForm(forms.Form):
    content = UEditorField('内容',
                           width=600, height=300, toolbars="full", imagePath="static/images/",
                           filePath="static/files/",
                          upload_settings={"imageMaxSize":1204000},
                          settings={})
# Create your views here.
def login(request):#登陆界面
    return render(request,"server/index/login.html")
def loginHandler(request):#登陆管理
    username=request.POST.get("username")
    password=request.POST.get("password")
    #和数据库进行比较
    result=models.admin.objects.values("password","username").filter(username=username)
    if result.count()==1:
        if result[0]["password"]==password:
            request.session["admin"]=username
            return HttpResponse(returnResult.returnResult(0, "登陆成功"))
        else:
            return HttpResponse(returnResult.returnResult(1, "密码错误"))
    else:
        return HttpResponse(returnResult.returnResult(1, "没有此用户"))
def index(request):#首页
    username = request.session.get("admin")
    return render(request, "server/index/index.html", {"username": username})
    # if request.session.get("admin"):
    #     return render(request, "index/index.html", {"username": username})
    # else:
    #     return redirect("/")
def quit(request):#清除缓存，进入登陆页面
    request.session.flush()
    return redirect("/server/login/")


###############菜单

def menuList(request):#菜单列表
    username = request.session.get("admin")
    menuList=models.menu.objects.values("id","name").all()
    # print(menuList)
    return render(request,"server/menu/menuList.html",{"menuList":menuList,"username":username})
def menuManage(request):#菜单管理页面
    username = request.session.get("admin")
    return render(request,"server/menu/menuManage.html",{"username":username})
def menuHandler(request):#管理添加菜单
    menuName=request.POST.get("menutitle")
    print(menuName)
    # 查找name类是否有添加的菜单名
    if menuName=="":
        return HttpResponse(returnResult.returnResult(1,"菜单名不能为空"))
    list = models.menu.objects.filter(name=menuName)
    if list.count()==0:
        try :
            print("该菜单名不存在")
            addMenuName = models.menu(name=menuName)
            addMenuName.save()
            return HttpResponse(returnResult.returnResult(0,"提交成功"))
        except Exception as e:
            return HttpResponse(returnResult.returnResult(1,"提交失败"))
    if menuName==list[0].name:
        print("该菜单名已存在")
        return HttpResponse(returnResult.returnResult(1,"该菜单名已存在"))
    else:
        try :
            print("该菜单名不存在")
            addMenuName = models.menu(name=menuName)
            addMenuName.save()
            return HttpResponse(returnResult.returnResult(0,"提交成功"))
        except Exception as e:
            return HttpResponse(returnResult.returnResult(1,"提交失败"))
def delMenuHandle(request):#管理删除菜单
    menuid=request.GET.get("menuid")
    try:
        models.menu.objects.filter(id=menuid).delete()
        return HttpResponse(returnResult.returnResult(0, "删除成功"))
    except Exception as e:
        return HttpResponse(returnResult.returnResult(1, "删除失败"))
def editMenu(request):#编辑菜单页面
    username = request.session.get("admin")
    mid=request.get_full_path().split("=")[1]
    menuInfo=models.menu.objects.filter(id=mid).all()
    return render(request,"server/menu/editMenu.html",{"name":menuInfo[0].name,"username":username})
def editMenuHandler(request):#编辑菜单提交
    mid=request.POST.get("menuId")
    menutitle=request.POST.get("menutitle")
    try:
        models.menu.objects.filter(id=mid).update(name=menutitle)
        return HttpResponse(returnResult.returnResult(0, "修改成功"))
    except Exception as e:
        return HttpResponse(returnResult.returnResult(1, "修改失败"))

######################文章


def articleList(request):#文章列表页面
    username = request.session.get("admin")
    page=1
    catId=-1
    keyTitle=""
    if request.GET.get("page"):
        page=int(request.GET.get("page"))
        print("页码",page)
    if request.GET.get("catId"):
        catId = int(request.GET.get("catId"))
        print("菜单id", catId)
    if request.GET.get("keyTitle"):
        keyTitle=request.GET.get("keyTitle")
        print("关键字", keyTitle)
    if catId == -1:
        allCount = models.news.objects.filter(title__contains=keyTitle).count()
    else:
        allCount = models.news.objects.filter(catid=catId,title__contains=keyTitle).count()
    everyPage = 3#每屏显示条数
    startIndex=(int(page)-1)*everyPage
    endIndex=int(page)*everyPage
    print("总条数", allCount)
    print("页数", page)
    pages = math.ceil(allCount / 3)  # 总页数
    allPages = math.ceil(allCount / everyPage)#总页码
    dic=returnResult.getView(allPages, page)
    startPage=dic["startPage"]
    endPage=dic["endPage"]
    allPageList=range(startPage,endPage)
    # getView(currentPage, allCount, startIndex, endIndex)
    print(allPageList)
    menuList=models.menu.objects.values("id","name").all()
    if catId == -1:
        newsList = models.news.objects.filter(title__contains=keyTitle).all().order_by("-id")[startIndex:endIndex]
    else:
        newsList = models.news.objects.filter(catid=catId,title__contains=keyTitle).all().order_by("-id")[startIndex:endIndex]
    print("查到的结果",newsList)
    road=os.path.join(os.getcwd(),"static/uploads/img")
    for item in newsList:
        file = os.path.join(road,item.thumb)
        print(file)
        if not os.path.exists(file):
            item.thumb=None
        result=filter(lambda x: x['id'] == item.catid,menuList)
        catList=list(result)
        if catList:
            item.catname=catList[0]["name"]
    print(newsList)
    positionList=models.position.objects.all()
    return render(request,"server/article/articleList.html",{"username":username,"articleList":newsList,"menuList":menuList,"allPageList":allPageList,"page":page,"catId":catId,"keyTitle":keyTitle,"positionList":positionList,"pages":pages})
def addArticle(request):#添加文章页面
    form=TestUEditorForm()
    username = request.session.get("admin")
    columnList = models.menu.objects.values("id","name").all()
    return render(request,"server/article/addArticle.html",{"form":form,"colorList":settings.color_list,"columnList":columnList,"username":username})
def articleHandler(request):#添加文章管理
    title=request.POST.get("title")
    thumb=request.FILES.get("headimg")
    color=request.POST.get("color")
    column=request.POST.get("column")
    content=request.POST.get('content')
    # print(request.POST)
    if title=="":
        return HttpResponse(returnResult.returnResult(1, "标题不能为空"))
    #将传过来的文件进行处理
    if request.FILES and thumb:
        imgSize = returnResult.getsize(thumb.size)
        #判断类型
        if thumb.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return HttpResponse(returnResult.returnResult(1, "文件类型错误"))
        if float(imgSize)>100:
            return HttpResponse(returnResult.returnResult(1, "文件过大"))
            # return HttpResponse(returnResult.returnResult(1,"文件过大"),content_type="application/json",charset="utf8")
            # data = {
            #     "code": 0,
            #     "msg": "文件过大"
            # }
            # return JsonResponse(data,charset="utf8")
        #将上传的图片写入文件
        filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + thumb.name.split("/")[-1]
        print(filename)
        #在写入文件之前判断存储路径是否存在
        road="static/uploads/img/"
        returnResult.judge(road)
        savePath = road + filename
        # 写入文件中
        with open(savePath, 'wb') as f:
            for file in thumb.chunks():
                f.write(file)
                f.flush()
        #有图片时写入数据库
        resultNews=models.news(title=title,catid=column,title_font_color=color,thumb=filename,num=0)
    #没有图片时写入数据库
    else:
        resultNews = models.news(title=title, catid=column, title_font_color=color, num=0)
    try:
        resultNews.save()
        time = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        resultNewsContent=models.news_content(newsid=resultNews.id,content=content,contentTime=time)
        resultNewsContent.save()
        return HttpResponse(returnResult.returnResult(0, "上传成功"))
    except Exception as e:
        return HttpResponse(returnResult.returnResult(1,"上传失败"))
def editArticle(request):#编辑文章页面
    username = request.session.get("admin")
    form = TestUEditorForm()
    articleId=request.get_full_path().split("=")[1]
    newsList=models.news.objects.values("id","catid","title","title_font_color","thumb","num").filter(id=articleId)
    newsContent=models.news_content.objects.values("id","newsid","content").filter(newsid=articleId)
    menuList=models.menu.objects.values("id","name")
    contentDetail=""
    road = os.path.join(os.getcwd(), "static/uploads/img")
    for item in newsList:
        print(item["title"])
        file = os.path.join(road, item["thumb"])
        print(file)
        if not os.path.exists(file):
            item["thumb"] = None
        content = filter(lambda x: x['newsid'] == item["id"], newsContent)
        news=list(content)
        if news:
            contentDetail=news[0]["content"]
            # print(item.content)
        menu=filter(lambda x:x["id"]==item["catid"],menuList)
        if menu:
            item["catname"]=list(menu)[0]["name"]
            # print(item.catname)
    return render(request, "server/article/editArticle.html", {"username": username,"form":form,"article":newsList,"colorList":settings.color_list,"menuList":menuList,"contentDetail":contentDetail})
def editHandler(request):#编辑文章提交
    aid=request.POST.get("aid")
    title = request.POST.get("title")
    thumb = request.FILES.get("headimg")
    color = request.POST.get("color")
    column = request.POST.get("column")
    content = request.POST.get('content')
    print(thumb)
    if thumb == None:
        thumb =request.POST.get("preImg")
    #删除原来的图片
    preImg=request.POST.get("preImg")
    if preImg:
        delPath="static/uploads/img/"+preImg
        delPath1=os.path.join(os.getcwd(),delPath)
        if os.path.exists(delPath1):
            os.remove(delPath1)
    if title == "":
        return HttpResponse(returnResult.returnResult(1, "标题不能为空"))
    # 将传过来的文件进行处理
    if request.FILES and thumb:
        imgSize = returnResult.getsize(thumb.size)
        # 判断类型
        if thumb.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return HttpResponse(returnResult.returnResult(1, "文件类型错误"))
        if float(imgSize) > 100:
            return HttpResponse(returnResult.returnResult(1, "文件过大"))
            # return HttpResponse(returnResult.returnResult(1,"文件过大"),content_type="application/json",charset="utf8")
            # data = {
            #     "code": 0,
            #     "msg": "文件过大"
            # }
            # return JsonResponse(data,charset="utf8")
        # 将上传的图片写入文件
        filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + thumb.name.split("/")[-1]
        print(filename)
        # 在写入文件之前判断存储路径是否存在
        road = "static/uploads/img/"
        returnResult.judge(road)
        savePath = road + filename
        # 写入文件中
        with open(savePath, 'wb') as f:
            for file in thumb.chunks():
                f.write(file)
                f.flush()
        # 有图片时写入数据库
        models.news.objects.filter(id=aid).update(title=title, catid=column, title_font_color=color, thumb=filename, num=0)
    # 没有图片时写入数据库
    else:
        models.news.objects.filter(id=aid).update(title=title, catid=column, title_font_color=color, num=0)
    try:
        time = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        models.news_content.objects.filter(newsid=aid).update(content=content, contentTime=time)
        return HttpResponse(returnResult.returnResult(0, "修改成功"))
    except Exception as e:
        return HttpResponse(returnResult.returnResult(1, "修改失败"))
def deleteArticle(request):#删除文章
    aid=request.GET.get("aid")
    try:
        models.news.objects.filter(id=aid).delete()
        models.news_content.objects.filter(newsid=aid).delete()
        return HttpResponse(returnResult.returnResult(0, "删除成功"))
    except Exception as e:
        return HttpResponse(returnResult.returnResult(1, "删除失败"))

##################推荐位管理

def positionList(request):#推荐位列表
    username = request.session.get("admin")
    positionList=models.position.objects.values("id","name").all()
    # print(menuList)
    return render(request,"server/position/positionList.html",{"positionList":positionList,"username":username})
def positionManage(request):#推荐位管理页面
    username = request.session.get("admin")
    return render(request,"server/position/positionManage.html",{"username":username})
def positionHandler(request):#推荐位添加菜单
    positionName=request.POST.get("positionName")
    print(positionName)
    # 查找name类是否有添加的菜单名
    if positionName=="":
        return HttpResponse(returnResult.returnResult(1,"菜单名不能为空"))
    list = models.position.objects.filter(name=positionName)
    if list.count()==0:
        try :
            print("该菜单名不存在")
            addpositionName = models.position(name=positionName)
            addpositionName.save()
            return HttpResponse(returnResult.returnResult(0,"提交成功"))
        except Exception as e:
            return HttpResponse(returnResult.returnResult(1,"提交失败"))
    if positionName==list[0].name:
        print("该菜单名已存在")
        return HttpResponse(returnResult.returnResult(1,"该菜单名已存在"))
    else:
        try :
            print("该菜单名不存在")
            addpositionName = models.position(name=positionName)
            addpositionName.save()
            return HttpResponse(returnResult.returnResult(0,"提交成功"))
        except Exception as e:
            return HttpResponse(returnResult.returnResult(1,"提交失败"))
def delPositionHandle(request):#管理删除推荐位
    positionid=request.GET.get("positionid")
    try:
        models.position.objects.filter(id=positionid).delete()
        return HttpResponse(returnResult.returnResult(0, "删除成功"))
    except Exception as e:
        return HttpResponse(returnResult.returnResult(1, "删除失败"))
def editPosition(request):#编辑推荐位页面
    username = request.session.get("admin")
    positionid=request.get_full_path().split("=")[1]
    positionInfo=models.position.objects.filter(id=positionid).all()
    return render(request,"server/position/editPosition.html",{"name":positionInfo[0].name,"username":username})
def editPositionHandler(request):#编辑推荐位提交
    positionid=request.POST.get("positionId")
    positiontitle=request.POST.get("positiontitle")
    try:
        models.position.objects.filter(id=positionid).update(name=positiontitle)
        return HttpResponse(returnResult.returnResult(0, "修改成功"))
    except Exception as e:
        return HttpResponse(returnResult.returnResult(1, "修改失败"))




#################推荐位内容管理
def positionContent(request):#推荐位内容管理页面
    username = request.session.get("admin")
    positionContentList=models.position_content.objects.all()
    positionName=models.position.objects.all()
    newsList=models.news.objects.all()
    for item in positionContentList:
        result=filter(lambda x:x.id==item.newsid,newsList)
        li=list(result)
        if li:
            item.title=li[0].title
            print(item.title)
        result1 = filter(lambda x: x.id == item.positionid, positionName)
        li1 = list(result1)
        if li1:
            item.name = li1[0].name
            print(item.name)
    return render(request,"server/positionContent/positionContent.html",{"username":username,"positionContentList":positionContentList})
def delPositionContentHandle(request):#删除推荐位内容管理
    positionid = request.GET.get("positionid")
    try:
        models.position_content.objects.filter(id=positionid).delete()
        return HttpResponse(returnResult.returnResult(0, "删除成功"))
    except Exception as e:
        return HttpResponse(returnResult.returnResult(1, "删除失败"))
def editPositionContent(request):
    positionlist = models.position.objects.all()
    id = request.GET.get("positionid")
    print(id)
    positionid = models.position_content.objects.values("positionid").filter(id=id).get()["positionid"]
    print(positionid)
    newsid = models.position_content.objects.values("newsid").filter(id=id).get()["newsid"]
    print(newsid)
    positionname = models.position.objects.filter(id=positionid)[0].name
    # print(positionname)
    return render(request, "server/positionContent/editPositionContent.html",
                  {"positionlist": positionlist, "positionname": positionname, "newsid": newsid})
def editreposHandler(request):
    newpositionid=request.POST.get("position")
    print(newpositionid)           #2
    newsid = request.POST.get("newsid")
    print(newsid)       #171
    models.position_content.objects.filter(newsid=newsid).update(positionid=newpositionid)
    return  HttpResponse(returnResult.returnResult(0,"修改成功"))






####################################基本管理
def basic(request):
    username = request.session.get("admin")
    return render(request,"server/basic/basic.html",{"username":username})
def clearAll(request):
    # 清理富文本编辑器里的无用图片
    imagesimg = os.listdir(os.path.join(os.getcwd(), "static/images"))
    content = models.news_content.objects.all()
    newcontentlist = []
    for item in content:
        content = item.content
        reg = '<img.*?src="(.*?\.(jpg|png|jpeg))".*?/>'
        m = re.findall(reg, content)
        if m != []:
            for item in m:
                imgName = item[0].split('/')[-1]
                print(imgName)
                newcontentlist.append(imgName)
    diffimages = list(filter(lambda x: x not in newcontentlist, imagesimg))
    if len(diffimages) != 0:
        for item in diffimages:
            os.remove("static/images/" + item)
            print("清除成功")
            return HttpResponse('<script>alert("清除成功")</script>')
    print("已经清理干净")
    return HttpResponse("<script>alert('已经清理干净')</script>")





######################用户管理
def userList(request):#用户页面
    username = request.session.get("admin")
    userList = models.admin.objects.all()
    return render(request,"server/user/userList.html",{"userList":userList,"username":username})
def addUser(request):#添加用户页面
    form = TestUEditorForm()
    return render(request,"server/user/addUser.html",{"form":form})
def userHandler(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    email=request.POST.get("email")
    headImg=request.FILES.get("headimg")
    useinfo=request.POST.get("content")
    userList=models.admin.objects.filter(username=username)
    if userList:
        return HttpResponse(returnResult.returnResult(1, "该用户名已存在"))
    if headImg == None:
        headImg =request.POST.get("preImg")
    #删除原来的图片
    preImg=request.POST.get("preImg")
    if preImg:
        delPath="static/uploads/img/"+preImg
        delPath1=os.path.join(os.getcwd(),delPath)
        if os.path.exists(delPath1):
            os.remove(delPath1)
    if username == "":
        return HttpResponse(returnResult.returnResult(1, "用户名不能为空"))
    # 将传过来的文件进行处理
    if request.FILES and headImg:
        imgSize = returnResult.getsize(headImg.size)
        # 判断类型
        if headImg.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return HttpResponse(returnResult.returnResult(1, "文件类型错误"))
        if float(imgSize) > 100:
            return HttpResponse(returnResult.returnResult(1, "文件过大"))
        # 将上传的图片写入文件
        filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split("/")[-1]
        print(filename)
        # 在写入文件之前判断存储路径是否存在
        road = "static/uploads/img/"
        returnResult.judge(road)
        savePath = road + filename
        # 写入文件中
        with open(savePath, 'wb') as f:
            for file in headImg.chunks():
                f.write(file)
                f.flush()
        # 有图片时写入数据库
        resultUser= models.admin(username=username, password=password, email=email, img=filename, lasttime=datetime.now(), userInfo=useinfo)
    # 没有图片时写入数据库
    else:
        resultUser = models.admin(username=username, password=password, email=email, lasttime=datetime.now(), userInfo=useinfo)
    try:
        resultUser.save()
        return HttpResponse(returnResult.returnResult(0, "注册成功"))
    except Exception as e:
        return HttpResponse(returnResult.returnResult(1, "注册失败"))
def editUser(request):
    form = TestUEditorForm()
    uid=request.GET.get("uid")
    userList=models.admin.objects.filter(id=uid)
    userInfo=""
    for item in userList:
        userInfo=item.userInfo
    return render(request,"server/user/editUser.html",{"form":form,"userList":userList,"userInfo":userInfo,"uid":uid})
def editUserHandler(request):
    uid=request.POST.get("uid")
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")
    headImg = request.FILES.get("headimg")
    useinfo = request.POST.get("content")
    userList = models.admin.objects.filter(username=username)
    if userList:
        return HttpResponse(returnResult.returnResult(1, "该用户名已存在"))
    if username == "":
        return HttpResponse(returnResult.returnResult(1, "用户名不能为空"))
    # 将传过来的文件进行处理
    if request.FILES and headImg:
        imgSize = returnResult.getsize(headImg.size)
        # 判断类型
        if headImg.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return HttpResponse(returnResult.returnResult(1, "文件类型错误"))
        if float(imgSize) > 100:
            return HttpResponse(returnResult.returnResult(1, "文件过大"))
        # 将上传的图片写入文件
        filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split("/")[-1]
        print(filename)
        # 在写入文件之前判断存储路径是否存在
        road = "static/uploads/img/"
        returnResult.judge(road)
        savePath = road + filename
        # 写入文件中
        with open(savePath, 'wb') as f:
            for file in headImg.chunks():
                f.write(file)
                f.flush()
        # 有图片时写入数据库
        resultUser = models.admin.objects.filter(id=uid).update(username=username, password=password, email=email, img=filename,
                                  lasttime=datetime.now(), userInfo=useinfo)
    # 没有图片时写入数据库
    else:
        resultUser = models.admin.objects.filter(id=uid).update(username=username, password=password, email=email, lasttime=datetime.now(),
                                  userInfo=useinfo)
    return HttpResponse(returnResult.returnResult(0, "修改成功"))
def deleteUser(request):
    uid = request.GET.get("uid")
    try:
        models.admin.objects.filter(id=uid).delete()
        return HttpResponse(returnResult.returnResult(0, "删除成功"))
    except Exception as e:
        return HttpResponse(returnResult.returnResult(1, "删除失败"))



###################将文章设为推荐位
def addPosition(request):
    checkArr=request.POST.getlist("choose")
    positionId=request.POST.get("positionId")
    for item in checkArr:
        check=models.position_content.objects.filter(newsid=item,positionid=positionId).count()
        print(check)
        if check == 0:
            add=models.position_content(newsid=item,positionid=positionId)
            add.save()
            return HttpResponse(returnResult.returnResult(0, "推送成功"))
        else:
            return HttpResponse(returnResult.returnResult(1, "该文章已被推荐"))