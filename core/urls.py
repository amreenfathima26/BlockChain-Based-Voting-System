from django.urls import path
from . import views
from voting import views as voting_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('superadmin-login/', views.superadmin_login, name='superadmin_login'),
    path('superadmin-dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('delete-election/<int:election_id>/', voting_views.delete_election, name='delete_election'),
    path('delete-block/<int:block_id>/', views.delete_block, name='delete_block'),
]
