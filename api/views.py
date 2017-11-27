import requests
from django.utils.http import urlencode
from base.view_utils import render_to_json_response


def get_oembed_data(request):
    """
    Ajax view for getting content from oembed services without CORS problems.
    Parameters:
        url    = (required) Service endpoint to request oembed data
        width  = (optional) Required iframe width
        height = (optional) Required iframe height
    """
    url = request.GET.get('url')
    width = request.GET.get('width')
    height = request.GET.get('height')

    if url is None:
        error = {'error': "missing parameter 'url'"}
        return render_to_json_response(error, status=400)

    data = {}

    if width:
        data['width'] = width
    if height:
        data['height'] = height

    response = requests.get(url + '&' + urlencode(data))
    return render_to_json_response(response.json())
