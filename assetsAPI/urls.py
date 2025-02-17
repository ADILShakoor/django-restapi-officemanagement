from django.urls import path
from . import views

# app rotes   assetapi/

urlpatterns = [
    path("my-assets/",views.AssertViewGeneric.as_view()),
    path("my-assets/<int:pk>",views.singleAssetView.as_view()),
    path("assets/",views.AssertView.as_view(
        { 'get':"list","post":"create"})),
    path("assets/<int:pk>/",views.AssertView.as_view(
        {
           "get":"retrieve", 
           "put":"update",
           "patch":"partial_update",
           "delete":"destroy"
        }
    ))
   
]




# urlpatterns = [
# 	path('books', views.BookView.as_view(
#     	{
#         	'get': 'list',
#         	'post': 'create',
#     	})
# 	),
#     path('books/<int:pk>',views.BookView.as_view(
#     	{
#         	'get': 'retrieve',
#         	'put': 'update',
#         	'patch': 'partial_update',
#         	'delete': 'destroy',
#     	})
# 	)
# ]