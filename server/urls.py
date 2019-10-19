from django.urls import path

from . import views
urlpatterns = [
    path('login/', views.login),
    path('loginHandler/', views.loginHandler),
    path('index/', views.index),
    path('quit/', views.quit),


    path('menuList/', views.menuList),
    path('menuManage/', views.menuManage),
    path("menuHandler/", views.menuHandler),
    path("delMenuHandle/", views.delMenuHandle),
    path("editMenu/", views.editMenu),
    path("editMenuHandler/", views.editMenuHandler),


    path("articleList/", views.articleList),
    path("addArticle/", views.addArticle),
    path("articleHandler/",views.articleHandler),
    path("editArticle/",views.editArticle),
    path("editHandler/",views.editHandler),
    path("deleteArticle/",views.deleteArticle),

    path("positionList/",views.positionList),
    path("positionManage/",views.positionManage),
    path("positionHandler/",views.positionHandler),
    path("delPositionHandle/",views.delPositionHandle),
    path("editPosition/",views.editPosition),
    path("editPositionHandler/",views.editPositionHandler),
    path("positionContent/",views.positionContent),
    path("delPositionContentHandle/",views.delPositionContentHandle),
    path("editPositionContent/",views.editPositionContent),
    path("editreposHandler/",views.editreposHandler),

    path("addPosition/",views.addPosition),



    path("basic/",views.basic),
    path("clearAll/",views.clearAll),

    path("userList/",views.userList),
    path("addUser/",views.addUser),
    path("userHandler/",views.userHandler),
    path("editUserHandler/",views.editUserHandler),
    path("editUserHandler/",views.editUserHandler),
    path("deleteUser/",views.deleteUser),


]