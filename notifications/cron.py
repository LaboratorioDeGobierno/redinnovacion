# django_cron
from django_cron import CronJobBase, Schedule

# django
from django.utils import timezone

# models
from notifications.models import Notification
from events.models import Event


class NotifyIncomingEventCronJob(CronJobBase):
    RUN_AT_TIMES = ['11:30', ]

    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'notifications.NotifyIncomingEventCronJob'

    def do(self):
        events = Event.objects.filter(
            start_date__gte=timezone.now() - timezone.timedelta(2),
            start_date__lte=timezone.now()
        )

        notifications = []

        for event in events:

            notification_kwargs = {
                'event': event,
                'kind': Notification.REMINDER,
            }

            user_ids = event.userevent_set.values_list('user_id', flat=True)

            for user_id in user_ids:
                notification_kwargs['user_id'] = user_id
                notifications.append(
                    Notification(**notification_kwargs)
                )

        Notification.objects.bulk_create(notifications)
