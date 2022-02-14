from django.urls import path

from . import views
urlpatterns = [
    path('',views.index, name= 'index'),
    path('product/<str:id>',views.product, name= 'product'),
    path('addtocart/<str:id>',views.addtocart, name= 'addtocart'),
    path('removeitemfromcart/<str:id>',views.removeitemfromcart, name= 'removeitemfromcart'),


    path('checkout/',views.checkout, name='checkout'),
    path('payment/<payment_option>/', views.paymentPage,name='payment'),

    path('ordersummary/',views.ordersummary, name= 'ordersummary'),
]