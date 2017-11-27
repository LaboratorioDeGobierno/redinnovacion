""" This document defines the UserManager class"""

# django
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Count
from django.db.models import F
from django.db.models import Q
from django.utils import timezone

# other
from base.managers import BaseManager

# enums
from users.enums import UserEnum


class UserQuerySet(models.QuerySet):
    def members(self):
        return self.filter(
            is_active=True,
            status=UserEnum.STATUS_ACCEPTED,
        )

    def top_active_users(self):
        """
        Returns top 3 active users by comments and activities
        """
        # exclude staff users
        users = self.select_related(
            'institution',
            'region',
        ).prefetch_related(
            'comment_set',
            'useractivity_set',
        ).exclude(
            is_staff=True,
        ).exclude(
            email__endswith='lab.gob.cl',
        )

        # only include active and accepted users
        # status 1 => Accepted
        users = users.members()
        users = users.filter(
            Q(comment__isnull=False) | Q(useractivity__isnull=False),
        )
        # calculate ranking and return top 3
        users = users.annotate(
            activity_count=Count('useractivity', distinct=True),
            comment_count=Count('comment', distinct=True)
        ).annotate(
            ranking=F('activity_count') + F('comment_count')
        ).order_by('-ranking')[:3]
        return users


class UserManager(BaseUserManager, BaseManager):
    """
    This class is used so the user manager has both the django defined
    user manager and the cusmtom defiled 'BaseManager
    ""
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def members(self):
        return self.get_queryset().members()

    def top_active_users(self):
        """
        Returns top 3 active users
        """
        return self.get_queryset().top_active_users()
