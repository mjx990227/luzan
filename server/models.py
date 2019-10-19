from django.db import models
# admin表（用来存放管理员用户数据的）
class admin(models.Model):
    username=models.CharField(max_length=20)#管理员名
    password=models.CharField(max_length=8)#密码
    email=models.CharField(max_length=50,null=True)#邮箱
    lasttime=models.DateTimeField()#最后一次登录时间
    img=models.CharField(max_length=100,null=True)#图片地址
    userInfo=models.TextField(null=True)#管理员介绍
    class Meta:
        db_table="admin"
# menu表（用来存放文章分类的）
class menu(models.Model):
    name=models.CharField(max_length=8)#菜单名
    class Meta:
        db_table="menu"
# news表（用来存放文章列表的）
class news(models.Model):
    catid=models.IntegerField()# 菜单id
    title=models.CharField(max_length=300)#新闻标题
    title_font_color=models.CharField(max_length=10)#颜色
    thumb=models.CharField(max_length=300)#缩略图
    num=models.IntegerField()#阅读数量
    class Meta:
        db_table="news"
# news_content表（用来存放每篇文章的详情）
class news_content(models.Model):
    newsid=models.IntegerField()
    content=models.TextField()#(文章内容)
    contentTime=models.DateTimeField()
    class Meta:
        db_table="news_content"
# position表（用来存放推荐位的分类的）
class position(models.Model):
    name=models.CharField(max_length=300)#推荐位名
    class Meta:
        db_table="position"
# position_content（用来存放不同推荐位下的文章id的）
class position_content(models.Model):
    positionid=models.IntegerField()#推荐位id
    newsid=models.IntegerField()#新闻id
    class Meta:
        db_table="position_content"

# Create your models here.
