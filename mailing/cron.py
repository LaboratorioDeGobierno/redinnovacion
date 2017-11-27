# django_cron
from django_cron import CronJobBase, Schedule

# models
from mailing.models import Mailing

import logging


class ScheduleMailingCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(
        run_every_mins=RUN_EVERY_MINS
    )
    code = 'mailing.schedule_mailing_cron_job'

    def do(self):
        unsent_mailings = Mailing.objects.filter(
            waiting_to_be_sent=True,
        )
        for mailing in unsent_mailings:
            data = mailing.mailchimp_list.get_mailchimp_data()
            if data['stats']['member_count'] > 0:
                schedule_response = mailing.schedule_using_mailchimp()

                # Mailchimp does not respond on success
                # so we assume it is scheduled on this scenario
                if not schedule_response:
                    mailing.waiting_to_be_sent = False
                    mailing.save()
                    continue

                logging.error(
                    "Error while scheduling campaign on mailchimp. "
                    + "Response: {}. Response status: {}.".format(
                        schedule_response, schedule_response['status']
                    )
                )
