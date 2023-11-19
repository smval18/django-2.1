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
    path('superadmin/', views.AdminPanelView.as_view(), name='superadmin'),
    path('superadmin/categories', views.CategoriesListView.as_view(), name='admin-categories'),
    path('superadmin/categories/create', views.CategoryCreateView.as_view(), name='admin-category-create'),
    path('superadmin/applications', views.ApplicationsListView.as_view(), name='admin-applications'),
    path('superadmin/categories/<pk>/delete', views.CategoryDeleteView.as_view(), name='admin-category-delete'),
    path('superadmin/applications/<pk>/update', views.ApplicationUpdateView.as_view(), name='admin-application-update'),






]