from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from institutions.models import Institution


class InstitutionForm(forms.ModelForm):

    class Meta:
        model = Institution
        fields = (
            'name',
            'url',
            'role_description',
            'logo',
            'kind',
        )
        labels = {
            'name': _("institution's name").capitalize(),
            'url':  _('website').capitalize(),
            'role_description': _('What is the role of this institution?'),
        }

    def save(self, commit=True):
        instance = super(InstitutionForm, self).save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.name)
        if commit:
            instance.save()
        return instance
