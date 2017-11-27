"""
This file has the Mockup class, that creates randomn instances of the
project models
"""

# standard library
import os
import random
import string
import uuid

# django
from django.utils import timezone
from django.apps import apps
from django.utils.text import slugify

# models
from activities.models import Activity, UserActivity
from cases.models import Case
from cases.models import CaseSearch
from cases.models import CaseSearchLog
from cases.models import CaseTag
from comments.models import Comment, CommentImage, CommentLike
from documentation.models import Documentation
from documentation.models import DocumentationFile
from documentation.models import DocumentationFileLog
from documentation.models import DocumentationSearch
from documentation.models import DocumentationSearchLog
from documentation.models import DocumentationTag
from documentation.models import Methodology
from documentation.models import Publication
from documentation.models import PublicationKind
from documentation.models import Tool
from documents.models import File, Photo
from dynamic_contents.models import DynamicContent
from evaluations.models import EventEvaluation
from events.models import Event, Stage, UserEvent
from institutions.models import Institution
from institutions.models import InstitutionKind
from interests.models import Interest
from mailing.models import EmailStatus
from mailing.models import EmailTarget
from mailing.models import EmailTemplate
from mailing.models import MailChimpCampaign
from mailing.models import MailChimpList
from mailing.models import Mailing
from mailing.models import TemplateImage
from messaging.models import EmailMessage
from notifications.models import Notification
from platforms.models import Platform, UserPlatformAttribute
from regions.models import Region, County
from users.models import User, TopicOfInterest
from newsletters.models import Newsletter
from newsletters.models import SentNewsletter

# utils
from base.utils import camel_to_underscore
from base.utils import random_string


class Mockup(object):
    def create_activity(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'event')
        return Activity.objects.create(**kwargs)

    def create_case(self, **kwargs):
        self.set_required_int(kwargs, 'year', minimum=0)
        return Case.objects.create(**kwargs)

    def create_case_search(self, **kwargs):
        self.set_required_string(kwargs, 'search')
        if 'slug' not in kwargs:
            kwargs['slug'] = slugify(kwargs['search'])
        return CaseSearch.objects.create(**kwargs)

    def create_case_search_log(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'user')
        self.set_required_foreign_key(
            kwargs,
            'case_search',
            model='case_search'
        )
        return CaseSearchLog.objects.create(**kwargs)

    def create_case_tag(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        if 'slug' not in kwargs:
            kwargs['slug'] = slugify(kwargs['name'])
        return CaseTag.objects.create(**kwargs)

    def create_comment(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'user')
        self.set_required_string(kwargs, 'text')
        return Comment.objects.create(**kwargs)

    def create_comment_image(self, **kwargs):
        # TODO mockup file field
        return CommentImage(**kwargs)

    def create_comment_like(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'comment')
        self.set_required_foreign_key(kwargs, 'user')
        return CommentLike.objects.create(**kwargs)

    def create_county(self, **kwargs):
        county = County.objects.first()
        if county:
            return county

        self.set_required_foreign_key(kwargs, 'region', model='region')
        return County.objects.create(**kwargs)

    def create_documentation(self, **kwargs):
        return Documentation.objects.create(**kwargs)

    def create_documentation_file(self, **kwargs):
        return DocumentationFile.objects.create(**kwargs)

    def create_documentation_file_log(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'user')
        return DocumentationFileLog.objects.create(**kwargs)

    def create_documentation_search(self, **kwargs):
        self.set_required_string(kwargs, 'search')
        return DocumentationSearch.objects.create(**kwargs)

    def create_documentation_search_log(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'user')
        self.set_required_foreign_key(
            kwargs,
            'documentation_search',
            model='documentation_search'
        )
        return DocumentationSearchLog.objects.create(**kwargs)

    def create_documentation_tag(self, **kwargs):
        return DocumentationTag.objects.create(**kwargs)

    def create_dynamic_content(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'created_by', model='user')
        self.set_required_foreign_key(kwargs, 'methodology')
        self.set_required_foreign_key(kwargs, 'tool')
        return DynamicContent.objects.create(**kwargs)

    def create_email_message(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'from_user', model='user')
        self.set_required_foreign_key(kwargs, 'to_user', model='user')
        self.set_required_string(kwargs, 'subject')
        self.set_required_string(kwargs, 'message')
        return EmailMessage.objects.create(**kwargs)

    def create_email_target(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'platform')
        self.set_required_string(kwargs, 'attribute_name')
        self.set_required_string(kwargs, 'attribute_value')
        return EmailTarget.objects.create(**kwargs)

    def create_email_status(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'user')
        self.set_required_foreign_key(kwargs, 'mailing')
        return EmailStatus.objects.create(**kwargs)

    def create_email_template(self, **kwargs):
        return EmailTemplate.objects.create(**kwargs)

    def create_event(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_foreign_key(kwargs, 'manager', model='user')
        self.set_required_foreign_key(kwargs, 'region')
        self.set_required_foreign_key(kwargs, 'county')
        self.set_required_string(kwargs, 'place')
        self.set_required_string(kwargs, 'address')
        self.set_required_datetime(kwargs, 'start_date')
        self.set_required_datetime(kwargs, 'end_date')
        return Event.objects.create(**kwargs)

    def create_event_evaluation(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'user')
        self.set_required_foreign_key(kwargs, 'event')
        self.set_required_int(kwargs, 'satisfaction', minimum=0, maximum=5)
        self.set_required_int(kwargs, 'usefulness', minimum=0, maximum=5)
        self.set_required_int(kwargs, 'clear_topics', minimum=0, maximum=5)
        self.set_required_string(kwargs, 'comments')
        self.set_required_string(kwargs, 'the_best')
        self.set_required_string(kwargs, 'what_can_be_improved')
        return EventEvaluation.objects.create(**kwargs)

    def create_file(self, **kwargs):
        return File.objects.create(**kwargs)

    def create_institution(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        if 'slug' not in kwargs:
            kwargs['slug'] = slugify(kwargs['name'])
        return Institution.objects.create(**kwargs)

    def create_institution_kind(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_int(kwargs, 'id', minimum=6)
        return InstitutionKind.objects.create(**kwargs)

    def create_interest(self, **kwargs):
        return Interest.objects.create(**kwargs)

    def create_mail_chimp_campaign(self, **kwargs):
        self.set_required_foreign_key(
            kwargs, 'mailing_list', model='mail_chimp_list',
        )
        return MailChimpCampaign.objects.create(**kwargs)

    def create_mail_chimp_list(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'mailing')
        return MailChimpList.objects.create(**kwargs)

    def create_mailing(self, **kwargs):
        self.set_required_foreign_key(
            kwargs, 'template', model='email_template',
        )
        return Mailing.objects.create(**kwargs)

    def create_methodology(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'documentation_file')
        return Methodology.objects.create(**kwargs)

    def create_newsletter(self, **kwargs):
        return Newsletter.objects.create(**kwargs)

    def create_notification(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'user')
        self.set_required_int(kwargs, 'kind', minimum=1, maximum=5)
        return Notification.objects.create(**kwargs)

    def create_photo(self, **kwargs):
        return Photo.objects.create(**kwargs)

    def create_platform(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        return Platform.objects.create(**kwargs)

    def create_publication(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'author', model='user')
        self.set_required_foreign_key(kwargs, 'documentation_file')
        return Publication.objects.create(**kwargs)

    def create_publication_kind(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        return PublicationKind.objects.create(**kwargs)

    def create_region(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        return Region.objects.create(**kwargs)

    def create_sent_newsletter(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'user')
        self.set_required_foreign_key(kwargs, 'newsletter')
        return SentNewsletter.objects.create(**kwargs)

    def create_stage(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'event')
        return Stage.objects.create(**kwargs)

    def create_tool(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'documentation_file')
        return Tool.objects.create(**kwargs)

    def create_topic_of_interest(self, **kwargs):
        return TopicOfInterest.objects.create(**kwargs)

    def create_template_image(self, **kwargs):
        self.set_required_foreign_key(
            kwargs, 'template', model='email_template',
        )
        return TemplateImage.objects.create(**kwargs)

    def create_user_activity(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'user')
        self.set_required_foreign_key(kwargs, 'activity')
        return UserActivity.objects.create(**kwargs)

    def create_user_event(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'user')
        self.set_required_foreign_key(kwargs, 'event')
        return UserEvent.objects.create(**kwargs)

    def create_user_platform_attribute(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'user')
        self.set_required_foreign_key(kwargs, 'platform')
        self.set_required_string(kwargs, 'name')
        self.set_required_string(kwargs, 'value')
        return UserPlatformAttribute.objects.create(**kwargs)

    def create_user_profile(self, **kwargs):

        if 'user' in kwargs:
            user = kwargs['user']
        else:
            user = self.create_user()

        user_profile = user.profile

        user_profile.update(**kwargs)
        return user_profile

    def create_user(self, password=None, **kwargs):
        if kwargs.get('first_name') is None:
            kwargs['first_name'] = self.random_string(length=6)

        if kwargs.get('last_name') is None:
            kwargs['last_name'] = self.random_string(length=6)

        if kwargs.get('email') is None:
            kwargs['email'] = "%s@gmail.com" % self.random_string(length=6)

        if kwargs.get('is_active') is None:
            kwargs['is_active'] = True

        if kwargs.get('slug') is None:
            kwargs['slug'] = self.random_string(length=10)

        user = User.objects.create(**kwargs)

        if password is not None:
            user.set_password(password)
            user.save()

        return user

    def random_email(self):
        return "{}@{}.{}".format(
            self.random_string(length=6),
            self.random_string(length=6),
            self.random_string(length=2)
        )

    def random_hex_int(self, *args, **kwargs):
        val = self.random_int(*args, **kwargs)
        return hex(val)

    def random_int(self, minimum=-100000, maximum=100000):
        return random.randint(minimum, maximum)

    def random_float(self, minimum=-100000, maximum=100000):
        return random.uniform(minimum, maximum)

    def random_string(self, length=6, chars=None):
        return random_string(length=length, chars=chars)

    def random_uuid(self, *args, **kwargs):
        chars = string.digits
        return uuid.UUID(''.join(random.choice(chars) for x in range(32)))

    def set_required_boolean(self, data, field, default=None, **kwargs):
        if field not in data:

            if default is None:
                data[field] = not not random.randint(0, 1)
            else:
                data[field] = default

    def set_required_date(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now().date()

    def set_required_datetime(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now()

    def set_required_email(self, data, field):
        if field not in data:
            data[field] = self.random_email()

    def set_required_float(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_float(**kwargs)

    def set_required_foreign_key(self, data, field, model=None, **kwargs):
        if model is None:
            model = field

        if field not in data and '{}_id'.format(field) not in data:
            data[field] = getattr(self, 'create_{}'.format(model))(**kwargs)

    def set_required_int(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_int(**kwargs)

    def set_required_ip_address(self, data, field, **kwargs):
        if field not in data:
            ip = '{}.{}.{}.{}'.format(
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
            )
            data[field] = ip

    def set_required_rut(self, data, field, length=6):
        if field not in data:
            rut = '{}.{}.{}-{}'.format(
                self.random_int(minimum=1, maximum=99),
                self.random_int(minimum=100, maximum=990),
                self.random_int(minimum=100, maximum=990),
                self.random_string(length=1, chars='k' + string.digits),
            )
            data[field] = rut

    def set_required_string(self, data, field, length=6):
        if field not in data:
            data[field] = self.random_string(length=length)

    def set_required_url(self, data, field, length=6):
        if field not in data:
            data[field] = 'http://{}.com'.format(
                self.random_string(length=length))


def add_get_or_create(cls, model):
    model_name = camel_to_underscore(model.__name__)

    def get_or_create(self, **kwargs):
        try:
            return model.objects.get(**kwargs), False
        except model.DoesNotExist:
            pass

        method_name = 'create_{}'.format(model_name)
        return getattr(cls, method_name)(self, **kwargs), True

    get_or_create.__doc__ = "Get or create for {}".format(model_name)
    get_or_create.__name__ = "get_or_create_{}".format(model_name)
    setattr(cls, get_or_create.__name__, get_or_create)


def add_create_many(cls, model):
    model_name = camel_to_underscore(model.__name__)

    def create_many(self, times, **kwargs):
        objects = []
        method_name = 'create_{}'.format(model_name)
        for i in range(times):
            objects.append(getattr(cls, method_name)(self, **kwargs))
        return objects

    create_many.__doc__ = "Create multiple copies of {}".format(model_name)
    create_many.__name__ = "create_{}s".format(model_name)
    setattr(cls, create_many.__name__, create_many)


def get_our_models():
    for model in apps.get_models():
        app_label = model._meta.app_label

        # test only those models that we created
        if os.path.isdir(app_label):
            yield model


for model in get_our_models():
    add_get_or_create(Mockup, model)
    add_create_many(Mockup, model)
