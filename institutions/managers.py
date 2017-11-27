from django.db import models


from base.managers import QuerySet


class InstitutionQueryset(QuerySet):

    def active(self):
        return self.filter(is_active=True)

    def has_users(self):
        return self.exclude(users__isnull=True)
