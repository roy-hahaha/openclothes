from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('ideas/', views.ideas, name='ideas'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path("selfie/", views.selfie, name="selfie"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('store/', views.store, name='store'),
    path('store/create/', views.create_store, name='create_store'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('search-store', views.search_stores, name='search-shops'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
