# standard library
import re

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

# third party
from easy_thumbnails.fields import ThumbnailerImageField
from random import randint

# models
from base.models import BaseModel
from base.models import file_path
from activities.models import Activity
from comments.managers import CommentQuerySet
from events.models import Event
from users.models import User
from notifications.models import Notification

# faker
from faker import Faker

MENTION_DELIMITER = '@'


class Comment(BaseModel):
    user = models.ForeignKey(
        User,
    )
    event = models.ForeignKey(
        Event,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    activity = models.ForeignKey(
        Activity,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    methodology = models.ForeignKey(
        'documentation.Methodology',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    tool = models.ForeignKey(
        'documentation.Tool',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    text = models.TextField(
        _('text'),
        max_length=600,
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    public = models.BooleanField(
        default=True,
    )
    images = models.ManyToManyField(
        'CommentImage',
        blank=True,
        verbose_name=_('images'),
    )
    user_mentions = models.ManyToManyField(
        User,
        blank=True,
        verbose_name=_('user mentions'),
        related_name='comment_mentions',
    )
    highlighted = models.BooleanField(
        default=False,
        verbose_name=_('highlighted'),
    )

    objects = CommentQuerySet.as_manager()

    class Meta:
        ordering = ('-updated_at',)

    def get_absolute_url(self):
        if self.event_id:
            return reverse(
                'event_detail', kwargs={
                    'pk': self.event_id,
                    'comment_id': self.pk,
                }
            )

        return reverse(
            'home', kwargs={
                'comment_id': self.pk,
            }
        )
        return ''

    @staticmethod
    def get_parsed_content(content, users):
        """
        Returns a string with user slugs transformed into their ids
        """
        text = unicode(content)
        users_dict = {user.slug: user for user in users}
        pattern = r'(?<=' + MENTION_DELIMITER + r')[\w-]+'

        for match in re.finditer(pattern, text):
            slug = match.group()
            user = users_dict.get(slug, None)
            if user:
                text = text.replace(
                    MENTION_DELIMITER + slug,
                    MENTION_DELIMITER + str(user.id),
                )

        return text

    def get_mentioned_ids(self):
        """
        Returns a list of mentioned ids
        """
        pattern = r'(?<=' + MENTION_DELIMITER + r')\w[\w-]*'

        ids = []

        for match in re.finditer(pattern, self.text):
            ids.append(int(match.group()))

        return ids

    def hide(self):
        self.public = False
        self.save()

    def public_children(self):
        return self.comment_set.filter(public=True)

    @classmethod
    def generate(cls, quantity, users):
        fake = Faker()
        user_count = len(users)
        comments = []
        for i in range(quantity):
            comment = {
                'user': users[randint(0, user_count)],
                'text': fake.text(),
                'highlighted': True,
                'public_children': {
                    'count': randint(0, 20)
                },
                'commentlike_set': {
                    'count': randint(0, 20)
                }
            }
            comments.append(comment)

        return comments


class CommentImage(BaseModel):
    exclude_on_on_delete_test = True
    # foreign keys
    # required fields
    image = ThumbnailerImageField(
        upload_to=file_path,
    )

    def get_absolute_url(self):
        return ''


class CommentLike(BaseModel):
    comment = models.ForeignKey(
        Comment,
    )
    user = models.ForeignKey(
        User,
    )

    class Meta:
        unique_together = ('comment', 'user')
        ordering = ('-id',)


@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, **kwargs):
    if created:
        notification_kwargs = {
            'comment': instance,
            'from_user_id': instance.user_id,
            'url': reverse('home'),
            'kind': Notification.RESPONSE,
        }

        if instance.parent_id:
            if instance.user_id == instance.parent.user_id:
                # do noting if it's the same user
                return

            instance.parent.update(updated_at=instance.updated_at)
            notification_kwargs['event_id'] = instance.parent.event_id
            notification_kwargs['user_id'] = instance.parent.user_id

            Notification.objects.create(**notification_kwargs)

        for user_id in instance.get_mentioned_ids():
            if not user_id:
                continue

            if instance.user_id == user_id:
                # do noting if it's the same user
                return

            if instance.parent_id and instance.parent.user_id == user_id:
                # do noting if we already notified a reply
                return

            notification_kwargs['kind'] = Notification.MENTION
            notification_kwargs['user_id'] = user_id
            Notification.objects.create(**notification_kwargs)
