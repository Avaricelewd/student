from django.urls import  path
from django.urls import path,include
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    # path('add/',views.index,name='add'),
    path('add/',views.add,name='add'),
    path('do_add/',views.do_add,name='do_add'),
    # path('update/',views.index,name='update'),
    path('<int:id>/update/',views.update,name='update'),
    path('<int:id>/do_update/',views.do_update,name='do_update'),
    # path('delete/',views.index,name='delete'),
    path('<int:id>/delete/',views.delete,name='delete'),
    path('export_excel/',views.export_excel,name='export_excle'),
    path('select/',views.select,name = 'select'),
    path('api_index/',views.api_index,name='api_index')

]





# 大多数情况两种方式可互换
# 如果参数就一个，且与业务关系较大，适合动态url匹配方式.  bili.com/av/58888  后台匹配path(av/<av_id>) . 视图函数的参数获取到。
# 方式二：参数较多，适合query string ， url后? 传参。
# bili.com/news/?page_no=2&page_size=20 , path('news/') ,视图韩式中request.GET['page_no']
