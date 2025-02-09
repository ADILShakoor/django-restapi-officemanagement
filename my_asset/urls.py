from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_assets, name='list_assets'),
    path('add_asset_category/', views.assert_category, name='assert_category'),
    path('add_or_assign_asset/', views.add_or_assign_asset, name='add_or_assign_asset'),
    path('<int:asset_id>/', views.asset_detail, name='asset_detail'),
    path("add_or_edit_asset/<int:asset_id>", views.add_or_edit_asset,name='add_or_edit_asset'),
    path("delete_asset/<int:asset_id>", views.delete_asset,name='delete_asset')

]
 