# standard
import json
import urlparse
import requests
import datetime

# settings
from django.conf import settings
from django.utils import timezone


class MailchimpAPIClient(object):
    def __init__(
        self,
        api_key=None,
        api_base_url=None,
        auth=None,
    ):
        if not api_key:
            self.api_key = settings.MAILCHIMP_API_KEY
        if not api_base_url:
            self.api_base_url = settings.MAILCHIMP_API_BASE_URL
        if not auth:
            self.auth = ('labgob', self.api_key)

    def ceil_dt(self, dt):
        minute = (dt.minute//15+1)*15
        return dt.replace(
            minute=0, second=0
        ) + datetime.timedelta(minutes=minute)

    def get(self, endpoint, payload=None):
        if payload is None:
            payload = {}

        return self.call_api('get', endpoint, payload)

    def post(self, endpoint, payload):
        return self.call_api('post', endpoint, payload)

    def put(self, endpoint, payload):
        return self.call_api('put', endpoint, payload)

    def call_api(self, method, endpoint, payload):
        url = urlparse.urljoin(self.api_base_url, endpoint).decode('utf-8')
        json_data = json.dumps(payload)

        if method == 'get':
            response = requests.get(
                url,
                auth=self.auth,
            )

        elif method == 'post':
            response = requests.post(
                url,
                data=json_data,
                auth=self.auth,
            )
        elif method == 'put':
            response = requests.put(
                url,
                data=json_data,
                auth=self.auth,
            )

        content = response.content

        try:
            content = json.loads(content)
        except:
            pass

        return content

    def get_list(self, list_id):
        endpoint = 'lists/{}/'.format(list_id)
        return self.get(endpoint)

    def get_lists(self):
        endpoint = 'lists/'
        return self.get(endpoint)

    def post_to_lists(self, payload):
        endpoint = 'lists/'
        return self.post(endpoint, payload)

    def post_to_campaigns(self, payload):
        endpoint = 'campaigns/'
        return self.post(endpoint, payload)

    def create_list_merge_field(self, list_id, payload):
        endpoint = 'lists/{}/merge-fields'.format(list_id)

        assert payload['name'], "Missing payload field 'name'"

        tag = payload.get('tag')
        if tag:
            if len(tag) > 10:
                print "WARNING: Mailchimp merge tags max length is 10."
                print "WARNING: Your tag will be shortened to '%s'" % tag[:10]
            payload['tag'] = tag.upper()
            reserved_tags = (
                'INTERESTS', 'UNSUB', 'FORWARD', 'REWARDS', 'ARCHIVE',
                'USER_URL', 'DATE', 'EMAIL', 'EMAIL_TYPE', 'TO'
            )
            assert payload['tag'] not in reserved_tags, "Payload field 'tag' "\
                "must not be in ({})".format(', '.join(reserved_tags))

        accepted_types = (
            'text', 'number', 'address', 'phone', 'date', 'url',
            'imageurl', 'radio', 'dropdown', 'birthday', 'zip',
        )
        assert payload['type'] in accepted_types, "Payload field 'type' " \
            "must be any between ({})".format(', '.join(accepted_types))

        return self.post(endpoint, payload)

    def create_list(self, name, **kwargs):
        contact = kwargs.get(
            'contact',
            settings.MAILCHIMP_CONTACT_DICT
        )

        campaign_defaults = {
            'from_name': kwargs.get(
                'from_name',
                settings.MAILCHIMP_CAMPAIGN_DEFAULTS['from_name']
            ),
            'from_email': kwargs.get(
                'from_email',
                settings.MAILCHIMP_CAMPAIGN_DEFAULTS['from_email']
            ),
            'subject': kwargs.get(
                'from_subject',
                '',
            ),
            'language': kwargs.get(
                'language',
                settings.MAILCHIMP_CAMPAIGN_DEFAULTS['language']
            ),
        }

        payload = {}
        payload['name'] = name
        payload['contact'] = contact
        payload['campaign_defaults'] = campaign_defaults
        payload['permission_reminder'] = kwargs.get(
            'permission_reminder',
            settings.MAILCHIMP_PERMISSION_REMINDER
        )
        payload['email_type_option'] = kwargs.get(
            'email_type_option',
            settings.MAILCHIMP_EMAIL_OPTION
        )

        response = self.post_to_lists(payload)
        return response

    def sub_users_to_list(self, users, list_id, extra_data_fn=None, **kwargs):
        payload = dict(**kwargs)

        users = list(users)

        endpoint = 'lists/{}/'.format(list_id)

        for i in range(0, len(users), 400):
            email_obj_list = []

            _users = users[i:i+400]
            for user in _users:
                user_data = {
                    'email_address': user.email,
                    'merge_fields': {
                        'FNAME': user.first_name,
                        'LNAME': user.last_name,
                    },
                    'status': 'subscribed',
                }
                if extra_data_fn:
                    extra_data_fn(user_data['merge_fields'], user)
                email_obj_list.append(user_data)

            payload['members'] = email_obj_list

            response = self.post(endpoint, payload)
            print response.get('new_members', 'ERROR !!!!\n')  # DEBUG
        return response

    def create_campaign(self, template, mailchimp_list, **kwargs):
        payload = dict(**kwargs)

        payload['type'] = kwargs.get(
            'type',
            settings.MAILCHIMP_CAMPAIGN_TYPE
        )
        payload['recipients'] = {
            'list_id': mailchimp_list.external_id,
        }
        payload['settings'] = kwargs.get(
            'settings',
            settings.MAILCHIMP_CAMPAIGN_SETTINGS
        )
        payload['settings']['subject_line'] = template.subject

        return self.post_to_campaigns(payload)

    def campaign_content_edit(self, mailing, **kwargs):
        payload = dict(**kwargs)
        if not payload['plain_text']:
            payload['plain_text'] = mailing.template.text_content

        if not payload['html']:
            payload['html'] = mailing.template.html_body

        endpoint = 'campaigns/{}/content/'.format(
            mailing.mailchimplist.external_id
        )

        response = self.put(endpoint, payload)

        return response

    def create_campaign_content(self, template, campaign):
        payload = {}
        payload['plain_text'] = template.text_content
        payload['html'] = template.make_html_template()

        endpoint = 'campaigns/{}/content/'.format(
            campaign.external_id,
        )

        return self.put(endpoint, payload)

    def campaign_send(self, campaign, **kwargs):
        payload = {}
        endpoint = 'campaigns/{}/actions/send/'.format(campaign.external_id)

        return self.post(endpoint, payload)

    def campaign_schedule(self, campaign, time=None):
        payload = {}
        if not time:
            time = timezone.now()
            time += datetime.timedelta(minutes=15)

        ceiled_time = self.ceil_dt(time)
        time_string = ceiled_time.strftime("%Y-%m-%dT%H:%M:%S")

        payload['schedule_time'] = time_string
        #  "2017-02-04T19:13:00+00:00"
        endpoint = 'campaigns/{}/actions/schedule/'.format(
            campaign.external_id
        )

        return self.post(endpoint, payload)
