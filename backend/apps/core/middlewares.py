import json
from django.contrib import messages

CONTENT_TYPES = ["application/javascript", "application/json"]


class AjaxMessaging(object):
    """
    Middlware for JSON responses. It adds to each JSON response array with
    messages from django.contrib.messages framework.
    It allows handle messages on a page with javascript
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __convert_message(self, message):
        return {
            'level_tag': message.level_tag,
            'level': message.level,
            'message': message.message,
            'extra_tags': message.extra_tags,
        }

    def __call__(self, request):
        response = self.get_response(request)

        if request.is_ajax():
            if response['Content-Type'] in CONTENT_TYPES:
                try:
                    content = json.loads(response.content.decode())
                    assert isinstance(content, dict)
                except (ValueError, AssertionError):
                    return response

                content['django_messages'] = [
                    self.__convert_message(message)
                    for message in messages.get_messages(request)
                ]
                response.content = json.dumps(content)
        return response
