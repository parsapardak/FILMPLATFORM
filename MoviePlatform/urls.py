from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # مسیر پنل مدیریت
    path('', views.home, name='home'),  # مسیر صفحه اصلی
    path('accounts/login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),  # مسیر لاگین
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # مسیر لاگ‌اوت
    path('', include('main.urls')),  # مسیرهای اپلیکیشن main
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)