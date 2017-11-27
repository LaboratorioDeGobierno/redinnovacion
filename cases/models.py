# -* - coding: utf-8 -*-

# standard library
import datetime

# django
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

# base
from base.models import BaseModel
from base.models import file_path

# models
from regions.models import Region
from users.models import User

# fields
from easy_thumbnails.fields import ThumbnailerImageField

# emails
from messaging import email_manager


class Case(BaseModel):
    title = models.CharField(
        _('title'),
        max_length=255,
        default='',
    )
    about = models.TextField(
        _('about'),
        default='',
    )
    logo = ThumbnailerImageField(
        _('logo'),
        upload_to=file_path,
        null=True,
        blank=True,
    )
    description_logo = models.TextField(
        _('description logo'),
        blank=True,
    )
    year = models.PositiveIntegerField(
        _('year'),
        default=datetime.date.today().year
    )
    team = models.CharField(
        _('team'),
        max_length=255,
        blank=True,
    )
    partners = models.TextField(
        _('partners'),
        blank=True,
    )
    duration = models.CharField(
        _('duration'),
        max_length=255,
        blank=True,
    )
    region = models.ForeignKey(
        Region,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('region'),
    )
    author = models.ForeignKey(
        'users.User',
        verbose_name=_('author'),
        related_name='published_cases',
        null=True,
        on_delete=models.SET_NULL,
    )
    editor = models.ForeignKey(
        'users.User',
        verbose_name=_('editor'),
        related_name='edited_cases',
        null=True,
        on_delete=models.SET_NULL,
    )

    # many to many
    tags = models.ManyToManyField(
        'cases.CaseTag',
        blank=True,
        verbose_name=_('tags'),
    )
    tools = models.ManyToManyField(
        'documentation.Tool',
        blank=True,
        verbose_name=_('tools'),
    )
    attachments = models.ManyToManyField(
        'documents.File',
        blank=True,
        verbose_name=_('attachments'),
    )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """ Returns the canonical URL for the case object """
        return reverse('case_detail', args=(self.pk,))

    def add_tags(self, tags):
        # delete all tags from case
        self.tags.clear()

        # tags array
        case_tags = []
        for tag in tags:
            # check if the tag exists
            slug_tag = slugify(tag.strip())
            case_tag, _ = CaseTag.objects.get_or_create(
                slug=slug_tag,
                defaults={
                    'name': tag,
                }
            )

            # append to tags array
            case_tags.append(case_tag)

        # add tags to case
        self.tags.add(*case_tags)

        # delete unused tags
        CaseTag.delete_unused_tags()

    def get_string_tags(self):
        """
        Returns a concatenation of tags names
        """
        str_tags = self.tags.values_list('name', flat=True)
        return u', '.join(str_tags)

    def get_team(self):
        """
        Returns team as list
        """
        return map(unicode.strip, self.team.split(','))

    def get_partners(self):
        """
        Returns partners as list
        """
        return map(unicode.strip, self.partners.split(','))

    def share(self, sender, users, message, use_https):
        """
        Send an email with the information of a documentation shared by a user
        """

        # email recipients
        users_emails = User.objects.filter(
            id__in=users
        ).values_list('email', flat=True)

        # context email
        context = {}
        context['sender'] = sender
        context['case'] = self
        context['message'] = message

        # add urls vars
        current_site = Site.objects.get_current()
        site_name = current_site.name
        domain = current_site.domain
        protocol = 'https' if use_https else 'http'
        context['site_name'] = site_name
        context['domain'] = domain
        context['protocol'] = protocol

        subject = u'[La Red] {} te ha compartido un caso'.format(
            sender.get_short_name(),
        )
        # send email
        email_manager.send_emails(
            emails=users_emails,
            template_name='case_share',
            subject=subject,
            context=context,
            fail_silently=False,
        )


class CaseTag(BaseModel):
    name = models.CharField(
        _('name'),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        _('slug'),
        unique=True,
        max_length=100,
        null=True,
    )

    def __unicode__(self):
        return u"{}".format(self.name)

    def save(self, *args, **kwargs):
        # if slug is not define or already exists, create a new one
        if (
            (not self.slug and self.name)
            or CaseTag.objects.filter(slug=self.slug).exists()
        ):
            self.slug = slugify(self.name)
            i = 1
            while CaseTag.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(slugify(self.name), i)
                i += 1
        super(CaseTag, self).save(*args, **kwargs)

    @classmethod
    def delete_unused_tags(cls):
        # select tags without documentation
        tags = cls.objects.filter(
            case__isnull=True,
        )
        tags.delete()


class CaseSearch(BaseModel):
    search = models.CharField(
        _('search'),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        _('slug'),
        unique=True,
        max_length=100,
        null=True,
    )

    highlighted = models.BooleanField(
        default=False,
        verbose_name=_('highlighted'),
    )

    def __unicode__(self):
        return u"{}".format(self.search)

    def save(self, *args, **kwargs):
        # if slug is not define or already exists, create a new one
        if (
            (not self.slug and self.search)
            or CaseSearch.objects.filter(slug=self.slug).exists()
        ):
            self.slug = slugify(self.search)
            i = 1
            while CaseSearch.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(slugify(self.search), i)
                i += 1
        super(CaseSearch, self).save(*args, **kwargs)


class CaseSearchLog(BaseModel):
    # foreign keys
    case_search = models.ForeignKey(
        CaseSearch,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('case search'),
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='case_searched',
    )

    def __unicode__(self):
        return u"{} searched {}".format(self.user, self.case_search)
