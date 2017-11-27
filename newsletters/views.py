# -*- coding: utf-8 -*-
""" Views for the newsletters application. """
# standard library

# django
from django.contrib.sites.models import get_current_site
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.base import TemplateView

# models
from .models import Newsletter
from events.models import Event
from comments.models import Comment
from users.models import User

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import NewsletterForm

# random


class NewsletterListView(BaseListView):
    """
    View for displaying a list of newsletters.
    """
    model = Newsletter
    template_name = 'newsletters/list.jade'
    permission_required = 'newsletters.view_newsletter'


class NewsletterCreateView(BaseCreateView):
    """
    A view for creating a single newsletters
    """
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletters/create.jade'
    permission_required = 'newsletters.add_newsletter'


class NewsletterDetailView(BaseDetailView):
    """
    A view for displaying a single newsletters
    """
    model = Newsletter
    template_name = 'newsletters/detail.jade'
    permission_required = 'newsletters.view_newsletter'

    def get_context_data(self, **kwargs):
        context = super(NewsletterDetailView, self).get_context_data(**kwargs)

        context['next_events'] = Event.objects.incomming()[:4]
        if self.object.comments.exists():
            context['comments'] = self.object.comments.all()
        else:
            context['comments'] = Comment.objects.unsent_highlighted()

        # add site and domain vars
        current_site = Site.objects.get_current()
        site_name = current_site.name
        domain = current_site.domain
        protocol = 'https' if self.request.is_secure() else 'http'
        context['site_name'] = site_name
        context['domain'] = domain
        context['protocol'] = protocol
        context['event_colors'] = Event.get_dict_event_colors()
        
        return context


class NewsletterSendEmailView(BaseDetailView):
    model = Newsletter
    template_name = 'newsletters/detail.jade'
    permission_required = 'newsletters.view_newsletter'

    def get(self, request, *args, **kwargs):
        newsletter = self.get_object()
        newsletter.send_newsletter(
            users=[request.user],
            comments=Comment.objects.unsent_highlighted(),
            store=False,
        )
        return redirect(reverse('newsletter_list'))


class NewsletterUpdateView(BaseUpdateView):
    """
    A view for editing a single newsletters
    """
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletters/update.jade'
    permission_required = 'newsletters.change_newsletter'


class NewsletterDeleteView(BaseDeleteView):
    """
    A view for deleting a single newsletters
    """
    model = Newsletter
    permission_required = 'newsletters.delete_newsletter'
    template_name = 'newsletters/delete.jade'

    def get_success_url(self):
        return reverse('newsletter_list')


class NewsletterScenarioView(TemplateView):
    template_name = "newsletters/generate.jade"

    def post(self, request, *args, **kwargs):
        # get post data
        num_events = int(request.POST.get('events', 0))
        num_comments = int(request.POST.get('comments', 0))
        unread_notifications = int(
            request.POST.get('unread_notifications', 0)
        )
        unread_messages = int(
            request.POST.get('unread_messages', 0)
        )

        # generate data
        users = User.generate(20)
        events = Event.generate(num_events)
        comments = Comment.generate(num_comments, users)
        newsletter = Newsletter.get_newsletter()

        # send_email
        if 'send_email' in request.POST:
            newsletter.send_newsletter(
                users=[request.user],
                store=False,
                events=events,
                comments=comments,
                notifications=unread_notifications,
                messages=unread_messages,
            )
            return redirect(reverse('newsletter_scenario'))

        # render email template
        else:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            protocol = 'https' if request.is_secure() else 'http'
            context = {
                'next_events': events,
                'comments': comments,
                'unread_notifications': unread_notifications,
                'unread_messages': unread_messages,
                'user': request.user,
                'event_colors': Event.get_dict_event_colors(),
                'site_name': site_name,
                'domain': domain,
                'protocol': protocol,

            }
            return render(
                request,
                'emails/newsletter.html',
                context=context
            )
