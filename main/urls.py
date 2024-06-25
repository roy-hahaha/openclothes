from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('store/', views.store, name='store'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
