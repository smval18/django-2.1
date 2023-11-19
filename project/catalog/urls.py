from django.urls import path

from . import views


urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/logouted/', views.logouted, name='logouted'),
    path('myapplication/', views.MyAppsView.as_view(), name='myapplication'),
    path('myapplication/new', views.NewAppView.as_view(), name='newapplication'),
    path('myapplication/<pk>/delete', views.DeleteAppView.as_view(), name='deleteapplication'),






]