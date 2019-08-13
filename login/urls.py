from django.urls import path
from . import views




urlpatterns = [
    path('index/', views.index),
    path('register/', views.register),
    path('do_register/', views.do_register),
    path('register_check/',views.register_check),
    path('login/',views.login),
    path('do_login/',views.do_login),
    path('logout/',views.logout),
    path('verify_image/(\d+)/(\d+)/',views.verify_image,name='verify_image')
]
app_name = 'login_account'