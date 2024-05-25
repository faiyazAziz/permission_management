from django.urls import path
from . import views
from .views import (
    UserListView, UserCreateView, UserUpdateView, UserDeleteView,
    GroupListView, GroupCreateView, GroupUpdateView, GroupDeleteView,
    UserPermissionsUpdateView, GroupPermissionsUpdateView,AuditLogListView
)
# from .admin import my_admin_site

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),path('users/', UserListView.as_view(), name='user_list'),
    path('users/add/', UserCreateView.as_view(), name='user_add'),
    path('users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('users/permissions/<int:pk>/', UserPermissionsUpdateView.as_view(), name='user_permissions'),

    path('users/', UserListView.as_view(), name='user_list'),
    path('users/add/', UserCreateView.as_view(), name='user_add'),
    path('users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('users/permissions/<int:pk>/', UserPermissionsUpdateView.as_view(), name='user_permissions'),

    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/add/', GroupCreateView.as_view(), name='group_add'),
    path('groups/edit/<int:pk>/', GroupUpdateView.as_view(), name='group_edit'),
    path('groups/delete/<int:pk>/', GroupDeleteView.as_view(), name='group_delete'),
    path('groups/permissions/<int:pk>/', GroupPermissionsUpdateView.as_view(), name='group_permissions'),
    
    path('audit-logs/', AuditLogListView.as_view(), name='audit_log_list'),
]
