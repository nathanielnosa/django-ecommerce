from django.urls import path

from . import views


urlpatterns = [
    path('login',views.loginuser,name ="login"),
    path('register/',views.register,name ="register"),
    path('dashboard/',views.dashboard,name ="dashboard"),
    path('logout/',views.logoutuser,name ="logout"),
    
    
    path('editprofile/',views.editprofile,name ="editprofile"),

]