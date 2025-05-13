from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .models import CalendarEvent
from .forms import CalendarEventForm
from google_calendar_API.google_calendar import create_google_calendar_event, update_google_calendar_event, delete_google_calendar_event
from google.oauth2.credentials import Credentials
from django.contrib.auth.decorators import login_required
from google_calendar_API.google_calendar import get_google_flow

@login_required
def authorize_google_calendar(request):
    flow = get_google_flow()
    auth_url, state = flow.authorization_url(prompt='consent')
    request.session['state'] = state
    return redirect(auth_url)

@login_required
def oauth2callback(request):
    state = request.session.get('state')
    if not state:
        return HttpResponse("Session expired. <a href='/authorize-google/'>Try again</a>")

    flow = get_google_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    # Save credentials in session
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }

    
    return redirect('event-create')  # uses name from urls.py

@login_required
def calendar_event_create(request):
  if request.user=="team-lead" or request.user=="hr":
    if request.method == 'POST':
        form = CalendarEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user

            creds = get_credentials_from_session(request)
            if creds:
                event_data = {
                    'title': event.title,
                    'description': event.description,
                    'location': event.location,
                    'start_time': event.start_time,
                    'end_time': event.end_time,
                }
                google_event = create_google_calendar_event(creds, event_data)

                
                event.google_event_id = google_event.get('id')
                event.google_event_link = google_event.get('htmlLink')

                print(" Google Event Synced:", google_event)  # Debug print

            event.save()
            return redirect('event-list')
    else:
        form = CalendarEventForm()
    return render(request, 'google_calendar/event_form.html', {'form': form, 'action': 'Create'})




def get_credentials_from_session(request):
    creds_data = request.session.get('credentials')
    if not creds_data:
        return None
    return Credentials(**creds_data)


@login_required
def calendar_event_list(request):
    events = CalendarEvent.objects.filter(created_by=request.user)
    return render(request, 'google_calendar/event_list.html', {'events': events})


# @login_required
# def calendar_event_create(request):
#     if request.method == 'POST':
#         form = CalendarEventForm(request.POST)
#         if form.is_valid():
#             event = form.save(commit=False)
#             event.created_by = request.user

#             creds = get_credentials_from_session(request)
#             if creds:
#                 event_data = {
#                     'title': event.title,
#                     'description': event.description,
#                     'location': event.location,
#                     'start_time': event.start_time,
#                     'end_time': event.end_time,
#                 }
#                 google_event = create_google_calendar_event(creds, event_data)
#                 event.google_event_id = google_event.get('id')
#                 event.google_event_link = google_event.get('htmlLink')

#             event.save()
#             return redirect('event-list')
#     else:
#         form = CalendarEventForm()  
#     return render(request, 'google_calendar/event_form.html', {'form': form, 'action': 'Create'})


@login_required
def calendar_event_update(request, pk):
    
    event = get_object_or_404(CalendarEvent, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = CalendarEventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)

            creds = get_credentials_from_session(request)
            if creds and event.google_event_id:
                update_google_calendar_event(creds, event.google_event_id, form.cleaned_data)

            event.save()
            return redirect('event-list')
    else:
        form = CalendarEventForm(instance=event)
    return render(request, 'google_calendar/event_form.html', {'form': form, 'action': 'Update'})


@login_required
def calendar_event_delete(request, pk):
    event = get_object_or_404(CalendarEvent, pk=pk, created_by=request.user)
    if request.method == 'POST':
        creds = get_credentials_from_session(request)
        if creds and event.google_event_id:
            delete_google_calendar_event(creds, event.google_event_id)
        event.delete()
        return redirect('event-list')
    return render(request, 'google_calendar/event_confirm_delete.html', {'event': event})



@login_required
def sync_event_to_google(request, meeting_id):
    from google.oauth2.credentials import Credentials
    creds_data = request.session.get('credentials')

    if not creds_data:
        return redirect('authorize-google') 

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
