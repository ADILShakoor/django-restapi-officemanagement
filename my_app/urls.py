from django.urls import path
from . import views



urlpatterns = [
    # dashboard
    path('', views.create_account, name='create_account'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_users, name='search_users'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('view_self_asset/', views.view_self_asset, name='view_self_asset'),
    path('view_self_taskes/', views.view_self_taskes, name='view_self_taskes'),
    path('view_self_projects/', views.view_self_projects, name='view_self_projects'),
    path('view_self_leaves/', views.view_self_leaves, name='view_self_leaves'),
    path('view_self_attendances/', views.view_self_attendances, name='view_self_attendances'),
    
    path('manage_company_records/', views.manage_company_records, name='manage_company_records'),
    path('manage_team_records/', views.manage_team_records, name='manage_team_records'),
    path('view_self_record/', views.view_self_record, name='view_self_record'),
    path('edit/<int:user_id>/',views.edit_user , name="edit_user"),
    path('delete/<int:user_id>/',views.delete_user , name="delete_user"),
    
    path('view_self_document/', views.self_document, name='self_document'),
    path('view_self_document/<int:pk>/', views.self_document_detail, name='self-document-detail'),

]