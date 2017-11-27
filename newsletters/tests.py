import math

from django.test import TestCase
from django.core import mail

from newsletters.models import Newsletter
from newsletters.models import SentNewsletter
from users.models import User

from users.enums import UserEnum
from base.mockups import Mockup

from random import randint


class NewsletterTest(TestCase):

    def setUp(self):
        # cons
        self.total_users = randint(80, 100)
        self.page = 5
        self.newsletter = Newsletter.get_newsletter()

        # mockup
        self.mockup = Mockup()

        # create users
        for i in range(self.total_users):
            self.mockup.create_user(
                status=UserEnum.STATUS_ACCEPTED
            )

        self.users = User.objects.all()

    def test_send_newsletter(self):
        """ Test send_newsletter sends emails to users """
        # emails count
        count = 0
        for i in range(int(math.ceil(self.total_users * 1.0/self.page))):

            # how many emails will be send
            page_user = User.objects.members().exclude(
                newsletters__newsletter__in=[self.newsletter],
            )[:5].count()

            # sends emails
            Newsletter.send_todays_newsletter()

            # check email box and compare with emails count
            self.assertEqual(len(mail.outbox), count + page_user)

            # update emails count
            count += page_user

        page_user = User.objects.members().exclude(
            newsletters__newsletter__in=[self.newsletter],
        )[:5].count()

        # no remaining users to send emails
        self.assertEqual(page_user, 0)

        # already sended emails
        self.assertEqual(len(mail.outbox), self.total_users)

    def test_already_sended_newsletter(self):
        """ Test already send_newsletter sends emails to users """
        # has not been sent the newsletter
        total_emails_not_sended = User.objects.members().exclude(
            newsletters__newsletter__in=[self.newsletter],
        ).count()
        self.assertEqual(total_emails_not_sended, self.total_users)

        # the next bulk create implies the sending of a newsletter
        SentNewsletter.objects.bulk_create(
            [
                SentNewsletter(
                    user=user,
                    newsletter=self.newsletter
                )
                for user in self.users
            ]
        )

        # has been sent the newsletter
        total_emails_not_sended = User.objects.members().exclude(
            newsletters__newsletter__in=[self.newsletter],
        ).count()

        # no remaining users to send emails
        self.assertEqual(total_emails_not_sended, 0)
