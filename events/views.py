# -*- coding: utf-8 -*-
#
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView

# models
from activities.models import Activity
from events.models import Event, Stage, UserEvent
from regions.models import Region

# views
from base.views import BaseCreateView
from base.views import BaseListView, BaseUpdateView, BaseDetailView

# forms
from events.forms import EventForm, StageForm
from events.forms import EventStageForm

# serializers
from base.serializers import ModelEncoder

# dates
from dateutil import tz


class EventCreateView(BaseCreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_create.jade'
    navbar_active = 'activities'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context['stage_forms'] = self.stage_forms
        return context

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        form = super(EventCreateView, self).get_form(form_class)

        if not self.request.user.is_staff:
            form.exclude_staff_fields()

        stage_forms = []

        if self.request.user.is_staff:
            stage_types = Stage.STAGE_TYPES
        else:
            form.instance.activity_type = Event.ACTIVITY_TYPES.EXTERNAL
            stage_types_dict = dict(Stage.STAGE_TYPES)
            stage_types = (
                (
                    Stage.STAGE_TYPE_ACTIVITY,
                    stage_types_dict[Stage.STAGE_TYPE_ACTIVITY]
                ),
            )

        for stage_type, stage_title in stage_types:
            stage = Stage(
                name=stage_title,
                event=form.instance,
                stage_type=stage_type,
            )

            if self.request.method == "POST":
                stage_form = EventStageForm(
                    self.request.POST,
                    instance=stage,
                    prefix=stage_title,
                )
            else:
                stage_form = EventStageForm(
                    instance=stage,
                    prefix=stage_title,
                )
            stage_form.title = stage_title
            stage_forms.append(stage_form)

        self.stage_forms = stage_forms

        return form

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        for stage_form in self.stage_forms:
            if not stage_form.is_valid():
                return self.form_invalid(form)

        response = super(EventCreateView, self).form_valid(form)

        for stage_form in self.stage_forms:
            stage_form.instance.event = self.object
            stage = stage_form.save()

            if stage.stage_type == stage.STAGE_TYPE_ACTIVITY:
                self.object.start_date = stage.start_date
                self.object.end_date = stage.end_date
                self.object.save()

        event = self.object
        event.update(creator=self.request.user)

        Activity.objects.create(
            event=event,
            name=event.name,
            region_id=event.region_id,
            start_date=event.start_date,
            end_date=event.end_date,
            quota=event.quota,
        )

        if event.is_experimenta():
            event.add_experimenta_users()

        return response


class EventDeleteView(RedirectView):
    model = Event
    pattern_name = 'event_list'
    permission_required = 'events.delete_event'
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(
            EventDeleteView, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        self.delete_event(kwargs['pk'])
        return reverse(self.pattern_name)

    def delete_event(self, pk):
        event = get_object_or_404(Event, pk=pk)
        event.is_active = False
        event.save()


class EventDetailView(BaseDetailView):
    model = Event
    template_name = 'events/event_detail.jade'
    context_object_name = 'event'
    navbar_active = 'activities'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)

        if self.object.is_experimenta():
            if (
                not self.request.user.is_experimenta()
                and not self.request.user.is_staff
            ):
                raise Http404

        activity = self.object.get_base_activity()
        current_stage = self.object.stage_set.active().get_current_stage()

        recent_events = Event.objects.filter(
            stage__stage_type=Stage.STAGE_TYPE_ACTIVITY,
            stage__is_active=True
        ).exclude(id=self.object.id)

        # exclude experimenta events if user is not in experimenta
        user = self.request.user
        if not user.is_experimenta() and not user.is_staff:
            recent_events = recent_events.exclude(
                activity_type=Event.ACTIVITY_TYPES.EXPERIMENTA
            )

        # Here we build a list of the event files with a flag indicating if
        # its name should be truncated. This is done by checking every word,
        # and # if any exceeds 30 chars (which is the minimum for small screens
        # to display it well), it gets truncated in the template.
        # Maybe this should be done with CSS, but I spent like an hour trying
        # to make it work, and I think this is enough
        files = []
        for file in self.object.files.all():
            words = file.get_filename().split()
            truncate = False

            for word in words:
                if len(word) > 30:
                    truncate = True
                    break

            files.append((file, truncate))

        comments = self.object.get_base_comments()

        comment_id = self.kwargs.get('comment_id')
        if comment_id:
            comment = comments.filter(id=comment_id).first()

            comments = list(comments.exclude(id=comment_id)[:9])

            if comment:
                comments.insert(0, comment)
        else:
            comments = list(comments[:10])

        context.update({
            'comments': comments,
            'activity': activity,
            'evaluation': self.object.eventevaluation_set.filter(
                user=self.request.user).first(),
            'evaluation_average': self.object.get_evaluation_average(),
            'recent_events': recent_events[:3],
            'stage': current_stage,
            'star_range': range(1, 6),
            'user_activity': self.request.user.useractivity_set.filter(
                activity=activity).first(),
            'files': files,
        })

        # mark event notifications as read
        self.object.notification_set.filter(
            user=self.request.user).update(read=True)

        return context


class EventListView(BaseListView):
    model = Event
    template_name = 'events/events_list.jade'
    navbar_active = 'activities'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        events = Event.objects.active()

        if not self.request.user.is_experimenta():
            events = events.exclude(
                activity_type=Event.ACTIVITY_TYPES.EXPERIMENTA
            )

        return events.annotate(
            activity_count=Count('activity'),
        )


class EventUpdateView(BaseUpdateView):
    model = Event
    form_class = EventForm
    permission_required = 'events.change_event'
    template_name = 'events/event_update.jade'
    navbar_active = 'activities'

    def check_permission_required(self):
        if self.request.user == self.get_object().creator:
            return True
        if self.request.user.is_staff:
            return True
        return super(EventUpdateView, self).check_permission_required()

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context['stage_forms'] = self.stage_forms
        return context

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        form = super(EventUpdateView, self).get_form(form_class)

        if not self.request.user.is_staff:
            form.exclude_staff_fields()

        stage_forms = []

        for stage in form.instance.stage_set.all():
            if self.request.method == "POST":
                stage_form = EventStageForm(
                    self.request.POST,
                    instance=stage,
                    prefix=stage.name,
                )
            else:
                stage_form = EventStageForm(
                    instance=stage,
                    prefix=stage.name,
                )
            stage_forms.append(stage_form)

        self.stage_forms = stage_forms

        return form

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        for stage_form in self.stage_forms:
            if not stage_form.is_valid():
                return self.form_invalid(form)

        response = super(EventUpdateView, self).form_valid(form)

        for stage_form in self.stage_forms:
            stage_form.instance.event = self.object
            stage = stage_form.save()

            if stage.stage_type == stage.STAGE_TYPE_ACTIVITY:
                self.object.start_date = stage.start_date
                self.object.end_date = stage.end_date
                self.object.save()

        event = self.object

        event.activity_set.update(
            name=event.name,
            region_id=event.region_id,
            start_date=event.start_date,
            quota=event.quota,
        )

        return response


class StageCreateView(BaseCreateView):
    model = Stage
    form_class = StageForm
    permission_required = 'events.add_stage'
    template_name = 'stage/stage_create.jade'
    navbar_active = 'activities'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StageCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(StageCreateView, self).get_form_kwargs()
        if 'data' in kwargs:
            event = Event.objects.get(pk=self.kwargs['event_pk'])
            kwargs['data']['event'] = event
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(StageCreateView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(pk=self.kwargs['event_pk'])
        return context


class StageDeleteView(RedirectView):
    model = Stage
    pattern_name = 'event_detail'
    permission_required = 'events.delete_stage'
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        stage_pk = kwargs.pop('pk')
        stage = self.delete_stage(stage_pk)
        kwargs['pk'] = stage.event.pk
        return super(StageDeleteView, self).dispatch(*args, **kwargs)

    def delete_stage(self, pk):
        stage = get_object_or_404(Stage, pk=pk)
        stage.is_active = False
        stage.save()
        return stage


class StageDetailView(BaseDetailView):
    model = Stage
    template_name = 'stage/stage_detail.jade'
    context_object_name = 'stage'
    navbar_active = 'activities'


class StageUpdateView(BaseUpdateView):
    model = Stage
    form_class = StageForm
    permission_required = 'events.change_stage'
    template_name = 'stage/stage_update.jade'
    navbar_active = 'activities'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StageUpdateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(StageUpdateView, self).get_form_kwargs()
        if 'data' in kwargs:
            event_pk = kwargs['data'].pop('event')[0]
            event = Event.objects.get(pk=event_pk)
            kwargs['data']['event'] = event
        return kwargs


class UserEventAttendView(RedirectView):
    model = UserEvent
    pattern_name = 'event_detail'
    permanent = False
    permission_required = 'events.change_userevent'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        user_event_pk = kwargs.pop('user_event_pk')
        user_event = self.attend_user_event(user_event_pk)
        kwargs['pk'] = user_event.event.pk
        return super(UserEventAttendView, self).dispatch(*args, **kwargs)

    def attend_user_event(self, user_event_pk):
        now = datetime.datetime.now()
        user_event = UserEvent.objects.get(pk=user_event_pk)
        user_event.attendance_date = now
        user_event.save()
        return user_event


@login_required
def events_calendar(request):
    context = {
        'regions': Region.objects.all(),
        'navbar_active': 'activities',
    }

    return render_to_response(
        'events/calendar.jade',
        context,
        context_instance=RequestContext(request)
    )


def get_event_data(request):
    """
    Provides events for fullcalendar.
    FullCalendar provides date range in request.GET

    Event structure:
        {
            'title': event title,
            'start': event start date,
            'end': event end date, //optional
            'allDay': True if the event duration is all day,  //optional
            'color': color event display,
            'type': sickday, vacation, holiday, birthday, event
        }

    return: a JSON with the events

    """
    tzinfo = tz.gettz('America/Santiago')
    start = request.GET.get('start')
    end = request.GET.get('end')

    if start is None or end is None:
        return JsonResponse([], encoder=ModelEncoder, safe=False)

    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    start = start.replace(tzinfo=tzinfo)
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    end = end.replace(tzinfo=tzinfo)

    region_id = request.GET.get('region')
    hide_events = request.GET.get('hideEvents')
    hide_workshops = request.GET.get('hideWorkshops')
    hide_meetings = request.GET.get('hideMeetings')
    hide_taks = request.GET.get('hideTaks')
    hide_external = request.GET.get('hideExternal')
    hide_experimenta = request.GET.get('hideExperimenta')

    events = Event.get_events_for_calendar(
        request.user,
        start,
        end,
        region_id=region_id,
        hide_events=hide_events,
        hide_workshops=hide_workshops,
        hide_meetings=hide_meetings,
        hide_taks=hide_taks,
        hide_external=hide_external,
        hide_experimenta=hide_experimenta,
    )

    return JsonResponse(events, encoder=ModelEncoder, safe=False)


def event_detail_with_login(request, pk, token, email):
    """
    Login with the token and redirect to the event detail
    """
    user = authenticate(email=email, password=None, token=token)

    if user:
        if user.is_active:
            login(request, user)

    event = get_object_or_404(Event, pk=pk)

    return HttpResponseRedirect(event.get_absolute_url())
