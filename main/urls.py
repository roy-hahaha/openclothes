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
    path('profile/', views.profile, name='profile', kwargs={'id': None}),
    path("profile/<int:id>/", views.profile, name="profile"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('store/', views.store, name='store'),
    path('store/create/<int:store_id>', views.create_store, name='create_store'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('product/create/<int:store_id>/', views.create_product, name='create_product'),
    path('search-store', views.search_stores, name='search-shops'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
