import json
import logging
import traceback

from django.http import Http404
from django.http.request import RawPostDataException
from django.utils.deprecation import MiddlewareMixin

# if you want to track it
# from sentry_sdk import capture_exception

logger = logging.getLogger()


def get_client_ip(request):
    """
    get client ip address

    used in:
        - apps/models_helper/visitor.py
    """
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ip_address:
        ip_address = ip_address.split(', ')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR', '')
    return ip_address


class SessionLogMiddleware(MiddlewareMixin):
    """
    this middleware to create a log
    by current user
    """

    def _logging(self, request, response=None, exception=None, status_code=None):

        headers = eval(str(request.headers))
        response_data = None
        request_data = None

        def clean_text(text):
            if isinstance(text, bytes):
                try:
                    return text.decode('utf-8') \
                        .replace('\\n', '') \
                        .replace('\\t', '') \
                        .replace('\\r', '')
                except Exception:
                    pass
            return str(text)

        try:
            request_data = json.loads(clean_text(request.body))
        except RawPostDataException:
            response_data = "RawPostDataException: You cannot access body after reading from request's data stream"
        except Exception:
            try:
                request_data = clean_text(request.body)
            except Exception:
                pass

        if not headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            try:
                response_data = json.loads(clean_text(response.content))
            except RawPostDataException:
                response_data = "RawPostDataException: You cannot access body after reading from request's data stream"
            except Exception:
                try:
                    response_data = clean_text(response.content)
                except Exception:
                    pass

        log_data = {
            'HEADERS': headers,
            'METHOD': request.method,

            'ip_address': get_client_ip(request),

            'URL': request.build_absolute_uri(),
            'REQUEST_DATA': request_data,
            'RESPONSE_DATA': response_data,
            'ERROR_MESSAGE': exception,
            'STATUS_CODE': status_code
        }

        logger.debug(log_data)

    def process_exception(self, request, exception):
        # print(type(exception), exception)  # just for debug
        status_code = 404 if isinstance(exception, Http404) else 500

        try:
            self._logging(request,
                             exception=exception,
                             status_code=status_code)
        except Exception as exc:
            # error = traceback.format_exc()
            # capture_exception(error)
            print(exc)

        return  # no return anything

    def process_response(self, request, response):
        if not response.status_code >= 400:
            try:
                response_data = {'request': request,
                                 'response': response,
                                 'status_code': response.status_code}
                self._logging(**response_data)
            except Exception:
                pass
        return response
