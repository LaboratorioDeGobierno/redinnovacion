# django
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

# standard library
import json
from base.models import ModelEncoder


def render_to_json_response(context, **response_kwargs):
    # returns a JSON response, transforming 'context' to make the payload
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(convert_context_to_json(context), **response_kwargs)


def convert_context_to_json(context):
    # convert the context dictionary into a JSON object
    # note: this is *EXTREMELY* naive; in reality, you'll need
    # to do much more complex handling to ensure that arbitrary
    # objects -- such as Django model instances or querysets
    # -- can be serialized as JSON.
    return json.dumps(context, cls=ModelEncoder)


def paginate(request, objects, page_size=25):
    paginator = Paginator(objects, page_size)
    page = request.GET.get('p')

    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_objects = paginator.page(paginator.num_pages)

    return paginated_objects


def clean_query_string(request):
    clean_query_set = request.GET.copy()

    clean_query_set = dict(
        (k, v) for k, v in request.GET.items() if not k.startswith('o_')
    )
    try:
        del clean_query_set['p']
    except:
        pass

    mstring = []
    for key in clean_query_set.iterkeys():
        valuelist = request.GET.getlist(key)
        mstring.extend(['%s=%s' % (key, val) for val in valuelist if val])

    return '&'.join(mstring)


def _add_message(request, tags, message):
    """
    Generic message
    """
    messages.add_message(
        request,
        tags,
        message
    )


def add_success_message(request, message):
    """
    Success message
    """
    _add_message(
        request,
        messages.SUCCESS,
        message
    )


def add_error_message(request, message):
    """
    Error message
    """
    _add_message(
        request,
        messages.ERROR,
        message
    )


def add_form_error_messages(request, form):
    """
    Multiple error messages
    """
    for field in form:
        for error in field.errors:
            add_error_message(
                request,
                u"{}: {}".format(unicode(field.label), error)
            )
