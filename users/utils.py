# -* - coding: utf-8 -*-

# django
from django.utils.text import slugify


def calculate_slug(first_name, last_name, mother_family_name, email, User):
    """
    This function calculate a slug name
    """
    slug = None
    i = 0
    # check if the values are defined
    if first_name or last_name or mother_family_name or email:
        # check if the slug is valid
        while not slug or User.objects.filter(slug=slug).exists():
            # generate slug using full name
            full_name = u'{} {} {}'.format(
                first_name,
                last_name,
                mother_family_name
            )
            slug = slugify(full_name)
            # if user doesn't have a full name replae with email
            if not slug:
                _email = email[:email.index(u'@')]
                slug = slugify(_email)
            # if this slug already exists add a number at the end
            # repeat until it is unique
            if i > 0:
                slug += u'-{}'.format(i)
            i += 1
    return slug
