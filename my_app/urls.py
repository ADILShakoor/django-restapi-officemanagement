from django.urls import path
from . import views



urlpatterns = [
    # Login, Logout, and Account Creation URLs
    path('', views.create_account, name='create_account'),
    path('login/', views.login_view, name='django-login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_users, name='search_users'),
    path('manage_company_records/', views.manage_company_records, name='manage_company_records'),
       # Team Lead View for Employee Records
    path('manage_team_records/', views.manage_team_records, name='manage_team_records'),
    # Employee View for Their Own Record
    path('view_self_record/', views.view_self_record, name='view_self_record'),
    path('edit/<int:user_id>/',views.edit_user , name="edit_user"),
    path('delete/<int:user_id>/',views.delete_user , name="delete_user")

]