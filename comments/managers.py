""" This document defines the CommentManager class"""

# django

# base
from base.managers import QuerySet


class CommentQuerySet(QuerySet):

    def public(self):
        return self.filter(public=True)

    def unsent_highlighted(self):
        return self.filter(highlighted=True, newsletter__isnull=True)

    def base_comments(self):
        return self.filter(parent=None).public()
