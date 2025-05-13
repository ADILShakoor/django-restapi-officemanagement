from django.urls import path
from . import views

urlpatterns = [
    path('authorize-google/', views.authorize_google_calendar, name='authorize-google'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('sync-event/', views.sync_event_to_google, name='sync-event'),
    path('events/', views.calendar_event_list, name='event-list'),
    path('events/create/', views.calendar_event_create, name='event-create'),
    path('events/<int:pk>/edit/', views.calendar_event_update, name='event-edit'),
    path('events/<int:pk>/delete/', views.calendar_event_delete, name='event-delete'),
    path('sync-event/<int:pk>/', views.sync_event_to_google, name='sync-event'),

]