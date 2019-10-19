import math
from django.shortcuts import render
from common import returnResult
from server import models
# Create your views here.
# # 首页导航
type_list=models.menu.objects.all()
# #侧栏小图
positionList1 = models.position.objects.filter(name="侧栏小图").values("id").all()
positionId1 = []
for item1 in positionList1:
    positionId1.append(item1["id"])
positionContentId1 = models.position_content.objects.filter(positionid__in=list(set(positionId1))).values("newsid").all()
newsId1 = []
for item1 in positionContentId1:
    newsId1.append(item1["newsid"])
newsList1 = models.news.objects.filter(id__in=list(set(newsId1)))[0:3]
# # 文章排行
newsList2=models.news.objects.all().order_by("-num")[0:5]
for item2 in newsList2:
    newsContent=models.news_content.objects.values("newsid","contentTime").all()
    result=filter(lambda x:x["newsid"] == item2.id,newsContent )
    timeList=list(result)
    if timeList:
        item2.contentTime=timeList[0]["contentTime"]
        print(item2.contentTime)
def index(request):#客户端首页
    #轮播图片
    positionList=models.position.objects.filter(name="首页大图").values("id").all()
    positionId=[]
    for item in positionList:
        positionId.append(item["id"])
    positionContentId=models.position_content.objects.filter(positionid__in=list(set(positionId))).values("newsid").all()
    newsId=[]
    for item in positionContentId:
        newsId.append(item["newsid"])
    newsList=models.news.objects.filter(id__in=list(set(newsId)))[0:3]
    #文章列表
    return render(request, "client/common/nav.html", {"type_list": type_list, "newsList": newsList, "newsList1": newsList1, "newsList2": newsList2})
def detail(request):
    newsId=request.GET.get("newsId")
    deatilNews=models.news_content.objects.filter(newsid=newsId).all()
    news=models.news.objects.filter(id=newsId).all()
    readnum=0
    for item in deatilNews:
        result=filter(lambda x:x.id == item.newsid,news)
        result1=list(result)
        if result1:
            item.title=result1[0].title
            item.num=result1[0].num
            readnum=result1[0].num+1
    models.news.objects.filter(id=newsId).update(num=readnum)
    return render(request, "client/detail.html", {"type_list": type_list, "newsList1": newsList1, "newsList2": newsList2,"deatilNews":deatilNews})
def column(request):
    columnId=request.GET.get("catid")
    print(columnId)
    page = int(request.GET.get("page"))
    print("页数", page)
    everyPage = 3  # 每屏显示条数
    startIndex = (int(page) - 1) * everyPage
    endIndex = int(page) * everyPage
    print(startIndex,endIndex)
    newsList = models.news.objects.filter(catid=columnId).all().order_by("-num")[startIndex:endIndex]
    print(newsList)
    allCount = models.news.objects.filter(catid=columnId).count()
    print("总条数", allCount)
    pages = math.ceil(allCount / 3)  # 总页数
    print("总页数",pages)
    allPages = math.ceil(allCount / everyPage)  # 总页码
    dic = returnResult.getView(allPages, page)
    startPage = dic["startPage"]
    endPage = dic["endPage"]
    allPageList = range(startPage, endPage)
    return render(request, "client/column.html",{"columnId":columnId,"page":page,"type_list": type_list, "newsList1": newsList1, "newsList2": newsList2,"newsList":newsList,"allPageList":allPageList,"pages":pages})