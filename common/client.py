from server import models
def common(type_list,newsList1,newsList2):
    # 首页导航
    type_list = models.menu.objects.all()
    # 侧栏小图
    positionList1 = models.position.objects.filter(name="侧栏小图").values("id").all()
    positionId1 = []
    for item1 in positionList1:
        positionId1.append(item1["id"])
    positionContentId1 = models.position_content.objects.filter(positionid__in=list(set(positionId1))).values(
        "newsid").all()
    newsId1 = []
    for item1 in positionContentId1:
        newsId1.append(item1["newsid"])
    newsList1 = models.news.objects.filter(id__in=list(set(newsId1))).all()
    # 文章排行
    newsList2 = models.news.objects.all().order_by("num")[0:5]
    for item2 in newsList2:
        newsContent = models.news_content.objects.values("newsid", "contentTime").all()
        result = filter(lambda x: x["newsid"] == item2.id, newsContent)
        timeList = list(result)
        if timeList:
            item2.contentTime = timeList[0]["contentTime"]
            print(item2.contentTime)