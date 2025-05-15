"""
URL configuration for office_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('my_app.urls')), # accounts/ 
    path('asset/',include('my_asset.urls')),
    path('project/', include('project_management.urls')),
    path('api/', include('accountsAPI.urls')),  # API routes
    path('assetapi/',include("assetsAPI.urls")),   #asset api routes
    path("projectAPI/",include("project_mangAPI.urls")),
    path('attendence/', include("attendence_management.urls")),
    path('attendenceAPI/', include("attendence_managementAPI.urls")),
    path("document-mng/",include('document_management.urls')),
    path('document-mngAPI/', include('document_managementAPI.urls')),
    path('', include('google_calendar_API.urls')),
    path('', include('google_calendar.urls')),  # calendar/
    path('jobMang/', include('jobMng.urls')),
    path('jobMangApi/', include('jobMngApi.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
