from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from base.views import BaseCreateView
from base.views import BaseUpdateView

from evaluations.models import EventEvaluation
from evaluations.forms import EventEvaluationForm

from activities.models import Activity
from events.models import Event


class EventEvaluationCreateView(BaseCreateView):
    model = EventEvaluation
    template_name = 'event_evaluations/create.jade'
    form_class = EventEvaluationForm

    def get_object(self, request, *args, **kwargs):
        if kwargs.get('event_id'):
            self.event_id = kwargs.get('event_id')
            self.activity_id = None

        if kwargs.get('activity_id'):
            self.activity_id = kwargs.get('activity_id')
            activity = Activity.objects.get(id=self.activity_id)
            self.event_id = activity.event_id

        try:
            obj = EventEvaluation.objects.get(
                user=request.user,
                event_id=self.event_id,
                activity_id=self.activity_id,
            )
        except EventEvaluation.DoesNotExist:
            obj = EventEvaluation(
                user=request.user,
                event_id=self.event_id,
                activity_id=self.activity_id,
            )
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(request, *args, **kwargs)

        if self.object.pk:
            return redirect(
                'event_evaluation_update',
                activity_id=kwargs.get('activity_id'),
                pk=self.object.pk,
            )

        return super(EventEvaluationCreateView, self).get(
            request, *args, **kwargs
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(request, *args, **kwargs)

        return super(EventEvaluationCreateView, self).post(
            request, *args, **kwargs
        )

    def get_form(self, form_class):
        form = super(EventEvaluationCreateView, self).get_form(form_class)

        form.instance.user = self.request.user
        form.instance.event_id = self.event_id
        form.instance.activity_id = self.activity_id

        return form

    def get_context_data(self, **kwargs):
        context = super(EventEvaluationCreateView, self).get_context_data(
            **kwargs
        )

        if self.kwargs.get('event_id'):
            context['event'] = Event.objects.get(id=self.kwargs['event_id'])

        if self.kwargs.get('activity_id'):
            context['activity'] = Activity.objects.get(
                id=self.kwargs['activity_id']
            )

        return context

    def get_success_url(self):
        if self.object.activity:
            return self.object.activity.get_absolute_url()

        if self.object.event:
            return self.object.event.get_absolute_url()

        return reverse('home')


class EventEvaluationUpdateView(BaseUpdateView):
    model = EventEvaluation
    template_name = 'event_evaluations/create.jade'
    form_class = EventEvaluationForm

    def get_context_data(self, **kwargs):
        context = super(EventEvaluationUpdateView, self).get_context_data(
            **kwargs
        )

        if self.kwargs.get('event_id'):
            context['event'] = Event.objects.get(id=self.kwargs['event_id'])

        if self.kwargs.get('activity_id'):
            context['activity'] = Activity.objects.get(
                id=self.kwargs['activity_id']
            )

        return context

    def get_success_url(self):
        if self.object.activity:
            return self.object.activity.get_absolute_url()

        if self.object.event:
            return self.object.event.get_absolute_url()

        return reverse('home')
