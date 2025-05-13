import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
from django.shortcuts import redirect
from django.http import HttpResponse
from .google_calendar import get_google_flow, create_google_calendar_event
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404
from google_calendar.models import CalendarEvent  # Update path based on your app name

# @login_required
# def authorize_google_calendar(request):
#     flow = get_google_flow()
#     auth_url, _ = flow.authorization_url(prompt='consent')
#     request.session['state'] = flow.state
#     return redirect(auth_url)

@login_required
def authorize_google_calendar(request):
    flow = get_google_flow()
    auth_url, state = flow.authorization_url(prompt='consent')

    request.session['state'] = state

    # Store meeting_id for redirect after authorization
    meeting_id = request.GET.get('meeting_id')
    if meeting_id:
        request.session['meeting_id'] = meeting_id

    return redirect(auth_url)

@login_required
def oauth2callback(request):
    state = request.session.get('state')
    if not state:
        return HttpResponse("Session expired or state missing. Please <a href='/authorize-google/'>try again</a>.")

    flow = get_google_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    meeting_id = request.session.pop('meeting_id', None)
    if meeting_id:
        return redirect('sync-event', meeting_id=meeting_id)

    return HttpResponse("Google Calendar connected!")


# @login_required
# def sync_event_to_google(request):
#     from google.oauth2.credentials import Credentials
#     creds_data = request.session.get('credentials')

#     if not creds_data:
#         return redirect('authorize-google')

#     creds = Credentials(**creds_data)

#     # Dummy Event — You can replace this with real event data from your model
#     event_data = {
#         'title': 'Test Meeting',
#         'description': 'Meeting synced with Google Calendar.',
#         'location': 'Zoom',
#         'start_time': timezone.now() + datetime.timedelta(hours=1),
#         'end_time': timezone.now() + datetime.timedelta(hours=2),
#     }

#     event = create_google_calendar_event(creds, event_data)
#     return HttpResponse(f"Event created: <a href='{event['htmlLink']}'>{event['summary']}</a>")
# google_calendar_API/views.py


@login_required
def sync_event_to_google(request, meeting_id):
    from google.oauth2.credentials import Credentials
    creds_data = request.session.get('credentials')

    if not creds_data:
        return redirect('authorize-google')  # Ensure user is authorized first

    creds = Credentials(**creds_data)

    meeting = get_object_or_404(CalendarEvent, id=meeting_id, created_by=request.user)

    event_data = {
        'title': meeting.title,
        'description': meeting.description,
        'location': meeting.location,
        'start_time': meeting.start_time,
        'end_time': meeting.end_time,
    }

    try:
        event = create_google_calendar_event(creds, event_data)
        meeting.calendar_event_id = event.get('id')
        meeting.save()
        return HttpResponse(f"Event synced: <a href='{event['htmlLink']}'>{event['summary']}</a>")
    except Exception as e:
        return HttpResponse(f"Error syncing event: {str(e)}")
