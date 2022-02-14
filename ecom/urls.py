from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('ecomm/', admin.site.urls),
    path('', include('stores.urls')), 
    path('users/', include('users.urls')), 

    # password reset
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='passwords/reset_password.html'), name="reset_password"),

    path('reset_password_send/',auth_views.PasswordResetDoneView.as_view(template_name='passwords/reset_password_sent.html'),name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='passwords/reset.html'),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='passwords/reset_password_complete.html'), name="password_reset_complete"),
    


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)