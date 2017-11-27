# -* - coding: utf-8 -*-

# standard library
import os
import uuid

# django
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_countries import countries

# base
from base.models import BaseModel
from base.models import file_path

# models
from users.models import User

# fields
from easy_thumbnails.fields import ThumbnailerImageField

# messaging
from messaging import email_manager


class DocumentationTag(BaseModel):
    name = models.CharField(
        _('name file'),
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
            or DocumentationTag.objects.filter(slug=self.slug).exists()
        ):
            self.slug = slugify(self.name)
            i = 1
            while DocumentationTag.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(slugify(self.name), i)
                i += 1
        super(DocumentationTag, self).save(*args, **kwargs)

    @classmethod
    def delete_unused_tags(cls):
        # select tags without documentation
        tags = cls.objects.filter(
            methodology__isnull=True,
            publication__isnull=True,
            tool__isnull=True,
        )
        tags.delete()


class DocumentationFile(BaseModel):
    name = models.CharField(
        _('name file'),
        max_length=255,
        default='',
    )
    archive = models.FileField(
        _('archive'),
        upload_to=file_path,
    )
    image = ThumbnailerImageField(
        _('file image'),
        upload_to=file_path,
        null=True,
        blank=True,
    )
    hash_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    def __unicode__(self):
        return u"{}".format(self.name)

    def get_file(self):
        """
        Custom function to get the file
        """
        return self.archive

    def extension(self):
        """
        Get archive extension
        """
        _, extension = os.path.splitext(self.archive.name)
        return extension

    def log_download(self, user):
        """
        Log user download
        """
        DocumentationFileLog.objects.get_or_create(
            documentation_file=self,
            user=user,
        )

    def get_documentfilelogs(self):
        """
        Return documentation file log, but with select_related.
        """
        return self.documentationfilelog_set.select_related('user')


class DocumentationFileLog(BaseModel):
    # foreign keys
    documentation_file = models.ForeignKey(
        DocumentationFile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('documentation file'),
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='documentation_downloaded',
    )

    def __unicode__(self):
        return u"{} downloaded {}".format(self.user, self.documentation_file)


class Documentation(BaseModel):
    """(Documentation description)"""
    title = models.CharField(
        _('title'),
        max_length=255,
        default='',
    )
    about = models.TextField(
        _('about'),
        default='',
    )
    description = models.TextField(
        _('description'),
        default='',
    )
    language = models.CharField(
        _('language'),
        blank=True,
        max_length=255,
        default='',
        choices=(
            (u'es', u'Español'),
            (u'en', u'Inglés'),
        )
    )
    country = models.CharField(
        _('country'),
        max_length=255,
        default='',
        blank=True,
        choices=countries,
    )

    # foreign keys
    documentation_file = models.ForeignKey(
        DocumentationFile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('documentation file'),
    )

    # many to many
    tags = models.ManyToManyField(
        DocumentationTag,
        blank=True,
        verbose_name=_('tags'),
    )

    class Meta:
        """ set to abstract """
        abstract = True

    def __unicode__(self):
        return u"{}".format(
            self.title,
        )

    def add_tags(self, tags):
        # delete all tags from documentation
        self.tags.clear()

        # tags array
        doc_tags = []
        for tag in tags:
            # check if the tag exists
            slug_tag = slugify(tag.strip())
            doc_tag, _ = DocumentationTag.objects.get_or_create(
                slug=slug_tag,
                defaults={
                    'name': tag,
                }
            )

            # append to tags array
            doc_tags.append(doc_tag)

        # add tags to documentation
        self.tags.add(*doc_tags)

        # delete unused tags
        DocumentationTag.delete_unused_tags()

    def get_string_tags(self):
        """
        Returns a concatenation of tags names
        """
        str_tags = self.tags.values_list('name', flat=True)
        return u', '.join(str_tags)

    def get_type_name(self):
        pass

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
        context['documentation'] = self
        context['message'] = message

        # add urls vars
        current_site = Site.objects.get_current()
        site_name = current_site.name
        domain = current_site.domain
        protocol = 'https' if use_https else 'http'
        context['site_name'] = site_name
        context['domain'] = domain
        context['protocol'] = protocol

        subject = u'[La Red] {} te ha compartido una {}'.format(
            sender.get_short_name(),
            self.get_type_name()
        )
        # send email
        email_manager.send_emails(
            emails=users_emails,
            template_name='documentation_share',
            subject=subject,
            context=context,
            fail_silently=False,
        )


class Methodology(Documentation):

    tools = models.ManyToManyField(
        'documentation.Tool',
        blank=True,
        verbose_name=_('tools'),
    )

    def __unicode__(self):
        return u"{}".format(
            self.title,
        )

    def get_absolute_url(self):
        """ Returns the canonical URL for the methodology object """
        return reverse('methodology_detail', args=(self.pk,))

    def get_type_name(self):
        return _(u"Methodology")

    def get_base_comments(self):
        comments = self.comment_set.base_comments()
        return comments.prefetch_related('comment_set', 'images')


class Tool(Documentation):
    how_to_use = models.TextField(
        _('how to use'),
        default='',
    )
    what_you_need = models.TextField(
        _('what you need'),
        default='',
    )
    image = ThumbnailerImageField(
        _('image'),
        upload_to=file_path,
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return u"{}".format(
            self.title,
        )

    def get_absolute_url(self):
        """ Returns the canonical URL for the tool object """
        return reverse('tool_detail', args=(self.pk,))

    def get_type_name(self):
        return _(u"Tool")

    def get_base_comments(self):
        comments = self.comment_set.base_comments()
        return comments.prefetch_related('comment_set', 'images')


class PublicationKind(BaseModel):
    name = models.CharField(
        _('name'),
        max_length=100,
        default='Publicación',
        unique=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('publication kind')
        verbose_name_plural = _('publication kinds')


class Publication(Documentation):
    # foreign keys
    kind = models.ForeignKey(
        PublicationKind,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('kind'),
    )

    # required fields
    short_description = models.CharField(
        _('short description'),
        max_length=50,
        default='',
    )
    highlighted = models.BooleanField(
        default=False,
        verbose_name=_('highlighted'),
    )
    author = models.CharField(
        _('author'),
        max_length=255,
        default='',
    )
    publication_date = models.DateField(
        _('publication date'),
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return u"{}".format(
            self.title,
        )

    def get_absolute_url(self):
        """ Returns the canonical URL for the publication object """
        return reverse('publication_detail', args=(self.pk,))

    def get_type_name(self):
        return _(u"Publication")

    def get_highlights(self):
        highlighted = Publication.objects.filter(
            highlighted=True
        ).exclude(
            id=self.id,
        ).select_related(
            'documentation_file',
        ).order_by(
            '-created_at',
        )
        return highlighted[:3]


class DocumentationSearch(BaseModel):
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
            or DocumentationSearch.objects.filter(slug=self.slug).exists()
        ):
            self.slug = slugify(self.search)
            i = 1
            while DocumentationSearch.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(slugify(self.search), i)
                i += 1
        super(DocumentationSearch, self).save(*args, **kwargs)


class DocumentationSearchLog(BaseModel):
    # foreign keys
    documentation_search = models.ForeignKey(
        DocumentationSearch,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('documentation search'),
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='documentation_searched',
    )

    def __unicode__(self):
        return u"{} searched {}".format(self.user, self.documentation_search)
