import json
import math
import os


def returnResult(code, msg, data=""):
    '''
    :param code: 0--success   ！=0  error
    :param msg: 信息
    :return:
    '''
    returndata = {
        "code": code,
        "msg": msg,
        "data": data
    }
    returndata1 = json.dumps(returndata)
    return returndata1
def getsize(size, format = 'kb'):
    p = 0
    if format == 'kb':
        p = 1
    elif format == 'mb':
        p = 2
    elif format == 'gb':
        p = 3

    size /= math.pow(1024, p)

    return "%0.2f"%size
def judge(dir):
    dirList=dir.split("/")
    # print(dirList,os.getcwd())
    for item,name in enumerate(dirList):
        itemDir=os.path.join(os.getcwd(),name)
        # print(itemDir)
        #判断当前文件夹是否存在
        if os.path.exists(itemDir):
            print("存在文件")
        else:
            os.mkdir(itemDir)

            # print("不存在文件")
        if item<len(dirList)-1:
            dirList[item+1]=name+"/"+dirList[item+1]
            print(dirList[item+1])
def getView(allPage,currentPage):
    # 当前页码，总页数，起始页，最后一页
    pageNow = currentPage  # 当前页码
    pages = allPage  # 总页数
    startPage = 1  # 起始页
    endPage = 1  # 最终页
    num = 3  # 要显示的页数
    if pageNow <= num / 2:
        startPage = 1
        endPage = num
    else:                   # 2-- 1.5-- 123
                            # 3-- 1.5 --234
        startPage = math.ceil(pageNow - num / 2)
        endPage = math.ceil(pageNow + num / 2-1)
    if endPage > pages:
        endPage = pages
        startPage = endPage - (num - 1)
    startPage=1 if startPage<1 else startPage
    return {"startPage": startPage, "endPage": endPage + 1}
