# django_cron
from django_cron import CronJobBase, Schedule

# models
from newsletters.models import Newsletter


class NewsletterMailingCronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'newsletters.schedule_newsletter_cron_job'

    def do(self):
        Newsletter.send_todays_newsletter()
