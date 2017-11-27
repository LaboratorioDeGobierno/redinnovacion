# standard library
import json

# django
from django.http import HttpResponse
from django.apps import apps
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext

from base.views import BaseCreateView
from base.views import BaseListView
from base.views import BaseUpdateView

from comments.models import Comment
from newsletters.models import Newsletter

from comments.forms import CommentForm
from comments.forms import CommentUpdateForm
from comments.forms import CommentLikeForm

from comments.models import CommentImage
from comments.forms import CommentImageForm
from comments.forms import CommentLike

from base.views import AjaxFormResponseMixin


Event = apps.get_model(app_label='events', model_name='Event')


class CommentListView(BaseListView):
    model = Comment
    template_name = 'comments/includes/list.jade'

    def get_queryset(self):
        updated_at = self.request.GET.get('updatedAt')
        event_id = self.request.GET.get('eventId')
        author_id = self.request.GET.get('authorId')
        comments = Comment.objects.filter(parent=None, public=True)

        if not self.request.user.is_experimenta():
            comments = comments.exclude(
                event__activity_type=Event.ACTIVITY_TYPES.EXPERIMENTA
            )

        if updated_at:
            comments = comments.filter(updated_at__lt=updated_at)

        # filter by id if present
        if event_id:
            comments = comments.filter(event_id=event_id)
        else:
            comments = comments.filter(event=None)

        # filter by id if present
        if author_id:
            comments = comments.filter(user_id=author_id)

        comments = comments[:3]

        return comments

    def get_context_data(self, **kwargs):
        context = super(CommentListView, self).get_context_data(**kwargs)
        context['comments'] = self.object_list
        context['event_id'] = self.request.GET.get('eventId')
        context['author_id'] = self.request.GET.get('authorId')
        return context


class CommentCreateView(AjaxFormResponseMixin, BaseCreateView):
    model = Comment
    template_name = 'comments/includes/detail.jade'
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(CommentCreateView, self).get_form(form_class)

        form.instance.user = self.request.user
        form.instance.public = True

        return form

    def form_valid(self, form):
        super(CommentCreateView, self).form_valid(form)

        context = {
            'comment': self.object
        }
        if not self.request.is_ajax():
            return redirect(self.request.META['HTTP_REFERER'])

        return render_to_response(
            self.template_name,
            context,
            context_instance=RequestContext(self.request)
        )


class CommentAnswerCreateView(AjaxFormResponseMixin, BaseCreateView):
    model = Comment
    template_name = 'comments/includes/detail_answer.jade'
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(CommentAnswerCreateView, self).get_form(form_class)

        form.instance.user = self.request.user
        form.instance.public = True

        return form

    def form_valid(self, form):
        super(CommentAnswerCreateView, self).form_valid(form)

        context = {
            'child_comment': self.object
        }

        if not self.request.is_ajax():
            return redirect(self.request.META['HTTP_REFERER'])

        return render_to_response(
            self.template_name,
            context,
            context_instance=RequestContext(self.request)
        )


class CommentHideView(SingleObjectMixin, RedirectView):
    model = Comment
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get('HTTP_REFERER')

    def get(self, request, *args, **kwargs):
        self.get_object().hide()
        return super(CommentHideView, self).get(request, *args, **kwargs)


class CommentUpdateView(AjaxFormResponseMixin, BaseUpdateView):
    model = Comment
    form_class = CommentUpdateForm

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.public = True
        # save
        self.object = form.save()

        if not self.request.is_ajax():
            return redirect(self.request.META['HTTP_REFERER'])

        context = {
            'comment': self.object
        }

        return render_to_response(
            'comments/includes/detail.jade',
            context,
            context_instance=RequestContext(self.request)
        )


class CommentImageCreateView(AjaxFormResponseMixin, BaseCreateView):
    model = CommentImage
    form_class = CommentImageForm

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


class CommentLikeCreateView(AjaxFormResponseMixin, BaseCreateView):
    model = CommentLike
    form_class = CommentLikeForm

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(CommentLikeCreateView, self).get_form(form_class)
        form.instance.user = self.request.user
        return form


def highlight_comment(request, comment_id=None):

    # get comment instance
    comment = Comment.objects.get(pk=comment_id)

    # update highlighted status
    comment.update(highlighted=not comment.highlighted)

    # add/remove highlighted comment from newsletter
    if comment.highlighted:
        # get next newsletter
        newsletter = Newsletter.get_newsletter()

        # add highlighted comment to next newsletter
        newsletter.comments.add(comment)
    else:
        # get newsletters from that comment
        newsletters = comment.newsletter_set.all()

        # remove highlighted comment from every newsletter
        for newsletter in newsletters:
            newsletter.comments.remove(comment)

    context = {
        'highlighted': comment.highlighted,
    }

    json_response = json.dumps(context)

    http_response = HttpResponse(json_response)
    http_response['Content-Length'] = len(http_response.content)
    http_response['Content-Type'] = "application/json"
    return http_response
