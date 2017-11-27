# -*- coding: utf-8 -*-
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

# models
from comments.models import Comment
from comments.models import CommentLike
from comments.models import CommentImage

# forms
from base.forms import BaseModelForm


class CommentForm(BaseModelForm):
    class Meta:
        model = Comment
        fields = (
            'text', 'event', 'activity', 'parent', 'images', 'user_mentions',
            'methodology', 'tool',
        )

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        text = cleaned_data.get('text', '')
        users = cleaned_data['user_mentions']
        cleaned_data['text'] = Comment.get_parsed_content(text, users)
        return cleaned_data


class CommentUpdateForm(BaseModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'event', 'activity', 'parent')


class CommentImageForm(BaseModelForm):
    class Meta:
        model = CommentImage
        fields = ('image',)


class CommentLikeForm(BaseModelForm):
    already_liked = _('you have already liked this comment')

    class Meta:
        model = CommentLike
        fields = ('comment',)

    def clean(self):
        likes = CommentLike.objects.filter(user=self.instance.user)
        likes = likes.filter(comment=self.cleaned_data['comment'])
        if likes.exists():
            raise ValidationError(self.already_liked)
        return super(CommentLikeForm, self).clean()
