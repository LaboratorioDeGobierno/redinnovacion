# -*- coding: utf-8 -*-

# standard library
import datetime

# django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import defaultfilters
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import RedirectView
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from base.views import BaseUpdateView, BaseDetailView
from base.views import BaseCreateView
from base.views import BasePDFView
from base.views import excel_response
from activities.forms import ActivityForm
from activities.forms import ActivityFilterForm
from activities.models import Activity, UserActivity
from events.models import Event
from events.models import Stage

# dates
from dateutil import tz


class ActivityCreateView(BaseCreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_create.jade'
    permission_required = 'activities.add_activity'
    navbar_active = 'activities'

    def form_valid(self, form):
        form.instance.event = Event.objects.get(pk=self.kwargs['event_pk'])
        return super(ActivityCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ActivityCreateView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(pk=self.kwargs['event_pk'])
        return context


class ActivityDeleteView(RedirectView):
    model = Activity
    pattern_name = 'event_detail'
    permanent = False
    permission_required = 'activities.delete_activity'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        activity_pk = kwargs.pop('pk')
        activity = get_object_or_404(Activity, pk=activity_pk)
        activity.deactivate()
        kwargs['pk'] = activity.event.pk
        return super(ActivityDeleteView, self).dispatch(*args, **kwargs)


class ActivityDetailView(BaseDetailView):
    model = Activity
    context_object_name = 'activity'
    template_name = 'activities/activity_detail.jade'
    navbar_active = 'activities'

    def dispatch(self, request, pk):
        self.object = self.get_object()
        return HttpResponseRedirect(
            reverse('event_detail', args=(self.object.event.pk,)),
        )

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data(**kwargs)
        context['event'] = context['activity'].event
        return context


class ActivityParticipantsView(BaseDetailView):
    model = Activity
    context_object_name = 'activity'
    template_name = 'activities/participants.jade'
    navbar_active = 'activities'

    def get_context_data(self, **kwargs):
        context = super(
            ActivityParticipantsView, self).get_context_data(**kwargs)

        if context['activity'].event.is_experimenta():
            if (
                not self.request.user.is_experimenta()
                and not self.request.user.is_staff
            ):
                raise Http404

        user_activities = UserActivity.objects.filter(
            activity=context['activity'],
        )

        context['useractivities'] = user_activities
        context['in_activity'] = user_activities.filter(
            user=self.request.user
        ).exists()
        return context


class ActivityUpdateView(BaseUpdateView):
    model = Activity
    form_class = ActivityForm
    permission_required = 'activities.change_activity'
    template_name = 'activities/activity_update.jade'
    navbar_active = 'activities'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ActivityUpdateView, self).dispatch(*args, **kwargs)


class UserActivityAttendView(RedirectView):
    model = UserActivity
    pattern_name = 'activity_participants'
    permanent = False
    permission_required = 'activities.change_useractivity'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        user_activity_pk = kwargs.pop('pk')
        user_activity = get_object_or_404(UserActivity, pk=user_activity_pk)
        user_activity.attend()
        kwargs['pk'] = user_activity.activity.pk
        return super(UserActivityAttendView, self).dispatch(*args, **kwargs)


class UserActivityCreateView(RedirectView):
    model = Activity
    pattern_name = 'activity_detail'
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        pk = kwargs.get('pk')
        user = self.request.user

        activity = get_object_or_404(Activity, pk=pk)
        registered, error = activity.register_assistant(user)

        if registered:
            user.send_activity_inscription_email(self.request, activity)
        elif error:
            messages.add_message(self.request, messages.ERROR, error)

        return super(UserActivityCreateView, self).dispatch(*args, **kwargs)


class UserActivityDeleteView(RedirectView):
    model = Activity
    pattern_name = 'activity_detail'
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        pk = kwargs.get('pk')
        user = self.request.user

        activity = get_object_or_404(Activity, pk=pk)
        deleted, error = activity.unregister_assistant(user)

        if deleted:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                "Se ha cancelado la inscripción"
            )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                error
            )

        return super(UserActivityDeleteView, self).dispatch(*args, **kwargs)


class ActivityCertificateView(SingleObjectMixin, BasePDFView):
    model = Activity

    template_name = 'activities/activity_certificate.jade'
    pdfkit_options = {
        'orientation': 'Landscape',
        'margin-top': '0.35in',
        'margin-right': '0.35in',
        'margin-bottom': '0.35in',
        'margin-left': '0.35in',
    }
    pdfkit_kwargs = {
        'css': [
            'base/static/bower_components/bootstrap/dist/css/bootstrap.css',
            'activities/static/css/activities/certificate.css'
        ]
    }

    def get_object(self, queryset=None):
        obj = super(ActivityCertificateView, self).get_object(
            queryset=queryset
        )
        if self.request.user not in obj.user_list():
            raise Http404
        return obj


class ExcelParticipants(View):

    def get(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        if not (
            request.user.is_staff or
            UserActivity.objects.filter(
                activity=activity,
                user=request.user,
            ).exists()
        ):
            raise Http404

        filename = u"{}_{}".format("inscritos", slugify(str(activity)))
        headers = (u"N°", "Nombre", u"Institución", "Correo", "Asiste")
        user_activities = UserActivity.objects.filter(
            activity=activity,
        )

        # create description
        if activity.start_date:
            start_date = timezone.localtime(activity.start_date)
        else:
            start_date = timezone.localtime(activity.event.start_date)
        end_date = timezone.localtime(
            activity.end_date if activity.end_date else activity.event.end_date
        )

        description = [
            activity.name,
            str(defaultfilters.date(start_date, u"d \d\e F \d\e Y")),
            u"{} a {} hrs".format(
                str(defaultfilters.date(start_date, "H\:i")),
                str(defaultfilters.date(end_date, "H\:i")),
            ),
            u"{}".format(activity.event.place),
        ]

        dataset = []
        i = 1
        for ua in user_activities:
            row = (
                i,
                u"{} {}".format(ua.user.first_name, ua.user.last_name),
                ua.user.institution,
                ua.user.email,
                u"si" if ua.attendance_date else u"no",
            )
            i = i + 1
            dataset.append(row)

        # get data
        return excel_response(filename, headers, dataset, description)


class ExcelGlobalParticipants(View):
    form_class = ActivityFilterForm
    template_name = 'activities/activity_report.jade'

    def get(self, request, *args, **kwargs):
        if not (
            request.user.is_staff
        ):
            raise PermissionDenied

        form = self.form_class()
        return render(
            request,
            self.template_name,
            {'form': form, 'navbar_active': 'global_report'}
        )

    def post(self, request):
        if not (
            request.user.is_staff
        ):
            raise PermissionDenied

        activities = Activity.objects.all()

        # TODO valid form
        # form = ActivityFilterForm(data=request.POST, empty_permitted=True)

        # get data from filters
        tzinfo = tz.gettz('America/Santiago')
        region_id = request.POST.get('region')
        activity_id = request.POST.get('activity')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        inscription_state = request.POST.get('inscription_state')

        # pythonize dates
        start = None
        if start_date:
            start = datetime.datetime.strptime(start_date, "%d/%m/%Y %H:%M")
            start = start.replace(tzinfo=tzinfo)

        end = None
        if end_date:
            end = datetime.datetime.strptime(end_date, "%d/%m/%Y %H:%M")
            end = end.replace(tzinfo=tzinfo)

        # filter region
        if region_id:
            activities = activities.filter(
                region_id=region_id
            )

        # filter activity
        if activity_id:
            activities = activities.filter(
                id=activity_id
            )

        # filter start date
        if start:
            activities = activities.filter(
                event__start_date__gte=start
            )

        # filter end date
        if end:
            if start:
                if end > start:
                    activities = activities.filter(
                        event__end_date__lte=end
                    )
            else:
                activities = activities.filter(
                    event__end_date__lte=end
                )

        # var filter inscription state
        filter_inscription = (
            str(inscription_state) == str(Stage.STAGE_TYPE_INSCRIPTION)
        )

        # info file
        filename = "{}".format("asistencia_global")
        headers = (
            "Nombre actividad",
            u"Región",
            "Fecha",
            "Lugar",
            "Stage",
            "Nombre",
            u"Institución",
            "Correo",
            u"Teléfono",
            "Cargo",
        )

        dataset = []
        for activity in activities:
            user_activities = UserActivity.objects.filter(
                activity=activity,
                stage__stage_type=Stage.STAGE_TYPE_INSCRIPTION
            )
            # filter by inscription state
            if inscription_state:
                user_activities = user_activities.filter(
                    attendance_date__isnull=filter_inscription
                )

            for ua in user_activities:
                row = (
                    activity.name,
                    activity.region,
                    defaultfilters.date(
                        activity.start_date, "d \d\e F \d\e Y"
                    ),
                    u"{}".format(activity.event.place),
                    u"Acreditación" if ua.attendance_date else u"Inscripción",
                    u"{} {}".format(ua.user.first_name, ua.user.last_name),
                    str(ua.user.institution if ua.user.institution else ""),
                    ua.user.email,
                    ua.user.phone if ua.user.phone else "",
                    ua.user.charge if ua.user.charge else ""
                )
                dataset.append(row)

        return excel_response(filename, headers, dataset)
