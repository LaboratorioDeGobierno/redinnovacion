# -*- coding: utf-8 -*-
""" Views for the messaging application. """
# standard library

# django
from django.db.models import Q
from django.db.models import Case
from django.db.models import When
from django.shortcuts import redirect

# models
from .models import EmailMessage
from users.models import User

# views
from base.views import AjaxFormResponseMixin
from base.views import BaseCreateView
from base.views import BaseListView

# forms
from .forms import EmailMessageForm


class EmailMessageListView(BaseListView):
    """
    View for displaying a list of messages.
    """
    model = EmailMessage
    template_name = 'email_messages/list.jade'
    ordering = ('-id',)
    title = 'Mensajes'

    paginate_by = 10

    def dispatch(self, *args, **kwargs):

        if 'user_pk' in self.kwargs:
            self.current_user = User.objects.get(pk=self.kwargs['user_pk'])
            if self.current_user.slug:
                return redirect('email_message_list', self.current_user.slug)
        elif 'slug' in self.kwargs:
            self.current_user = User.objects.get(slug=self.kwargs['slug'])
        else:
            # we need a current user, so search one in the lastest emails
            messages = super(EmailMessageListView, self).get_queryset()
            message = messages.filter_by_user(self.request.user).first()
            if message:
                # message was found, we need to find the interlocutor
                if message.from_user_id == self.request.user.id:
                    next_user = message.to_user
                else:
                    next_user = message.from_user

                # interlocutor found, redirect to messages with that user
                if next_user.slug:
                    return redirect(
                        'email_message_list',
                        next_user.slug
                    )
                else:
                    return redirect(
                        'email_message_list_by_pk',
                        next_user.id
                    )
            self.current_user = None

        return super(EmailMessageListView, self).dispatch(*args, **kwargs)

    def get_users(self):
        # obtain the interlocutors of the users messages
        messages = self.user_emails.order_by('-created_at')
        from_and_to_user_ids = messages.values_list(
            'from_user_id',
            'to_user_id'
        ).distinct()

        user_ids = []

        # get users that had comunications with the current user
        for from_user_id, to_user_id in from_and_to_user_ids:
            if to_user_id == self.request.user.id:
                user_id = from_user_id
            else:
                user_id = to_user_id

            if user_id not in user_ids:
                user_ids.append(user_id)

        # get users preserving order
        preserved = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(user_ids)]
        )
        self.users = User.objects.filter(pk__in=user_ids).order_by(preserved)

        # set current user
        if not self.current_user and self.users:
            self.current_user = self.users[0]

        # get user ids with unread messages
        self.user_ids_with_unread_messages = self.user_emails.filter(
            to_user=self.request.user,
            read=False,
        ).values_list('from_user_id', flat=True)

    def get_queryset(self):
        self.user_emails = super(EmailMessageListView, self).get_queryset()
        self.user_emails = self.user_emails.filter_by_user(self.request.user)

        self.users = []

        if self.request.is_ajax():
            self.template_name = 'email_messages/includes/messages_list.jade'
        else:
            self.get_users()

        # now filter our emails by the current user
        queryset = self.user_emails.filter(
            Q(from_user=self.request.user, to_user=self.current_user) |
            Q(to_user=self.request.user, from_user=self.current_user)
        ).order_by('-id')

        # filter by greater than  if set
        id__gt = self.request.GET.get('id__gt')
        if id__gt:
            queryset = queryset.filter(id__gt=id__gt)

        # filter by less than if set
        id__lt = self.request.GET.get('id__lt')
        if id__lt:
            queryset = queryset.filter(id__lt=id__lt)

        # select related
        queryset = queryset.select_related('from_user', 'to_user')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(EmailMessageListView, self).get_context_data(**kwargs)
        context['email_messages_by_dates'] = EmailMessage.group_by_date(
            context['object_list']
        )

        unread_senders = []
        read_senders = []

        # find users that sent us messages we have not read and separate
        for user in self.users:
            if user.id in self.user_ids_with_unread_messages:
                user.has_unread_messages = True
                unread_senders.append(user)
            else:
                read_senders.append(user)

        # list preserver order
        context['senders'] = unread_senders + read_senders

        # find users that sent us messages we have not read
        for user in context['senders']:
            if user.id in self.user_ids_with_unread_messages:
                user.has_unread_messages = True

        # find unread messages (to mark them as read)
        message_ids = []
        for message in context['object_list']:
            if message.from_user_id != self.request.user.id:
                message_ids.append(message.id)
        EmailMessage.objects.filter(id__in=message_ids).update(read=True)

        # Get the unread message list
        unread_messages = self.request.user.received_email_messages.filter(
            read=False
        )
        # replace the unread messages since we are marking them as read
        context['unread_messages'] = unread_messages.count()

        context['current_user'] = self.current_user
        context['no_messages'] = (len(context['email_messages_by_dates']) == 0)
        context['body_class'] = 'bg-color-gray-6'

        return context


class CreateEmailMessageCreateView(AjaxFormResponseMixin, BaseCreateView):
    model = EmailMessage
    form_class = EmailMessageForm

    def get_form(self, form_class):
        form = super(CreateEmailMessageCreateView, self).get_form(
            form_class
        )

        form.instance.from_user = self.request.user

        # check if the sender == receiver
        if int(self.request.POST['to_user']) == self.request.user.id:
            form.instance.read = True

        return form
