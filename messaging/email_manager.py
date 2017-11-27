# standard library

# django
from django.template import Template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from .smtp_email import send_email as stmp_send_email


def _send_emails(emails, subject, template_name=None, template_object=None,
                 sender=None, context=None, fail_silently=False,
                 attachments=None, headers=None):
    """ Sends an email to a list of emails using a given template name """
    if context is None:
        context = {}

    if attachments is None:
        attachments = []

    context = Context(context)

    if template_name:
        text_template = get_template("emails/%s.txt" % template_name)
        html_template = get_template("emails/%s.html" % template_name)
        text_content = text_template.render(context)
        html_content = html_template.render(context)

    if template_object:
        html_template = template_object.make_html_template()
        text_template = template_object.text_content
        html_content = Template(html_template).render(context)
        text_content = Template(text_template).render(context)

    if sender is None:
        sender = u"{} <{}>".format(
            settings.EMAIL_SENDER_NAME,
            settings.SENDER_EMAIL
        )

    if (settings.ENABLE_EMAILS and not settings.DEBUG) and not settings.TEST:
        # send email using stmp
        return stmp_send_email(
            emails, subject, html_content, text_content, sender, attachments
        )

    msg = EmailMultiAlternatives(
        subject, text_content, sender, emails, headers=headers,
    )

    for attachment in attachments:
        attachment.seek(0)
        msg.attach(attachment.name, attachment.read(),
                   'application/pdf')

    msg.attach_alternative(html_content, "text/html")

    msg.send(fail_silently=fail_silently)


def send_emails(**kwargs):
    """
    Sends an email to a list of emails using a given template name
    """
    _send_emails(**kwargs)


def send_example_email(email):
    """
    Sends an email to test the email funcionality.
    """
    subject = _("Hello")
    template_name = "example_email"

    send_emails(
        emails=(email,),
        template_name=template_name,
        subject=subject,
        context={},
    )
