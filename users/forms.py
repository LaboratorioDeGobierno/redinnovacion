# -*- coding: utf-8 -*-

# django
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import loader
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _
from django import forms

# models
from users.models import User, UserProfile
from base.models import BaseModel
from institutions.models import Institution

# forms
from base.forms import BaseModelForm
from captcha.fields import ReCaptchaField
from users.widgets import MtCheckboxInput


user_labels = {
    'address': u'Calle y número',
    'charge': u'¿Cuál es tu rol en tu institución?',
    'city': u'Ciudad',
    'county': u'Comuna',
    'description': (
        u'Cuentanos brevemente, ¿Qué te motiva a ser parte de la Red?'
    ),
    'email': u'¿Cuál es tu correo electrónico institucional?',
    'first_name': u'¿Cuál es tu primer nombre?',
    'institution': u'¿A qué institución pública perteneces?',
    'last_name': u'¿Cuál es tu apellido paterno?',
    'mother_family_name': u'¿Cuál es tu apellido materno?',
    'other_institution_name': u'¿Cuál es el nombre de tu institución?',
    'phone': u'¿Cuál es tu número de télefono de contacto?',
    'region': u'¿En qué región se encuentra tu institución?',
}


class AuthenticationForm(forms.Form):
    """ Custom class for authenticating users. Takes the basic
    AuthenticationForm and adds email as an alternative for login
    """
    email = forms.EmailField(label=_("Email"), required=True)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that both fields may be case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
        'pending': _('You must wait for an administrator to approve your '
                     'registration'),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        UserModel = get_user_model()
        self.email_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        validates the email and password.
        """
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': self.email_field.verbose_name},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
            elif (
                self.user_cache.status == User.STATUS_REJECTED
                or self.user_cache.status == User.STATUS_OTHER
            ):
                raise forms.ValidationError(
                    self.error_messages['pending'],
                    code='pending',
                )
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class CaptchaAuthenticationForm(AuthenticationForm):
    """ a user authentication form with a captcha """
    captcha = ReCaptchaField(
        label="¿Eres humano?",
    )


class AdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.

    """
    error_messages = {
        'required': _("Please log in again, because your session has expired.")
    }
    this_is_the_login_form = forms.BooleanField(
        widget=forms.HiddenInput, initial=1, error_messages=error_messages)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        message = _("Please enter the correct email and password for a staff "
                    "account. Note that both fields may be case-sensitive.")

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(message)
            elif not self.user_cache.is_active or not self.user_cache.is_staff:
                raise forms.ValidationError(message)

        return self.cleaned_data


class UserCreationForm(BaseModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    email = forms.EmailField(
        label=_("E-mail"), max_length=75,
        help_text=_("Enter the same password as above, for verification."),
    )
    first_name = forms.CharField(
        label=_("first name").capitalize(),
        help_text=_("The name of the user"),
    )
    last_name = forms.CharField(
        label=_("last name").capitalize(),
        help_text=_("The last name of the user"),
    )
    mother_family_name = forms.CharField(
        label=_("mother family name").capitalize(),
        required=False,
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput, required=False,
        help_text=_("Enter the same password as above, for verification."),
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'mother_family_name',
            'email',
            'charge',
            'region',
            'institution',
            'address',
            'county',
            'city',
            'phone',
            'is_staff',
            'status',
        )

        labels = user_labels

    def clean_email(self):
        """ checks that the email is unique """
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_password2(self):
        """ check that the password was correctly repeated """

        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, verify_email_address=False, domain_override=None,
             subject_template_name='emails/user_new_subject.txt',
             email_template_name='emails/user_new.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, commit=True):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.mother_family_name = self.cleaned_data["mother_family_name"]
        user.is_active = not verify_email_address

        if commit:
            user.save()

        if verify_email_address:
            from django.core.mail import send_mail

            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain

            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [user.email])

        return user


class UserInstitutionCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserInstitutionCreationForm, self).__init__(*args, **kwargs)
        del self.fields['institution']


class UserCreationCompleteForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationCompleteForm, self).__init__(*args, **kwargs)
        self.fields['institution'].queryset = Institution.objects.active()
        self.fields['institution'].empty_label = _('other').capitalize()
        self.fields['description'].widget = forms.Textarea(
            attrs={
                'rows': 4,
                'class': 'form-control',
                'maxlength': self.fields['description'].max_length,
            }
        )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'mother_family_name',
            'charge',
            'region',
            'institution',
            'other_institution_name',
            'email',
            'address',
            'county',
            'city',
            'phone',
            'description',
        )

        labels = user_labels

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            msg = UserCreationForm.error_messages['duplicate_email']
            raise forms.ValidationError(msg)
        return email


class CaptchaUserCreationForm(UserCreationForm):
    """ a user creation form with a captcha """
    captcha = ReCaptchaField(
        label="¿Eres humano?",
    )


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ('password',)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        self.fields['institution'].empty_label = _('other').capitalize()
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


class UserForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['institution'].queryset = Institution.objects.active()
        self.fields['institution'].empty_label = _('other').capitalize()
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 5})

        for field_name, field in self.fields.items():
            if hasattr(self.instance, field_name):
                if not getattr(self.instance, field_name):
                    field.required = False

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'mother_family_name',
            'institution',
            'other_institution_name',
            'address',
            'county',
            'city',
            'charge',
            'email',
            'phone',
            'interests',
            'description',
            'avatar',
            'region',
        )

        labels = user_labels


class UserImageForm(BaseModelForm):
    class Meta:
        model = User
        fields = (
            'avatar',
        )


class UserPasswordForm(BaseModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password = forms.CharField(
        label=_('New password'),
        required=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        help_text=_('Enter the same password as above, for verification.'),
        label=_('Password confirmation'),
        required=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('password',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        password = self.cleaned_data.pop('password')
        user = super(UserPasswordForm, self).save(commit=False)
        if password not in (u'', None, ''):
            user.set_password(password)
        if commit:
            user.save()
        return user


class UserProfileForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.itervalues():
            field.widget = MtCheckboxInput()

    class Meta:
        model = UserProfile
        fields = (
            'show_name',
            'show_charge',
            'show_institution',
            'show_email',
            'show_phone',
            'show_interests',
            'send_notifications_by_email',
        )


class UserProfileRegister(BaseModelForm):
    show_public_information = forms.BooleanField(
        widget=forms.RadioSelect(
            choices=BaseModel.BOOLEAN_CHOICES[::-1]),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(UserProfileRegister, self).__init__(*args, **kwargs)
        self.fields['topic_of_interests'].required = False

    class Meta:
        model = UserProfile
        fields = (
            'time_in_ri',
            'topic_of_interests',
            'other_topics',
            'show_public_information',
        )

        widgets = {
            'time_in_ri': forms.RadioSelect,
            'topic_of_interests': forms.CheckboxSelectMultiple,
        }
