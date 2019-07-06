# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from threading import current_thread

from django.utils.deprecation import MiddlewareMixin


_requests = {}


def get_request():
    t = current_thread()
    if t not in _requests:
        return None
    return _requests[t]


class RequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _requests[current_thread()] = request

    def process_response(self, request, response):
        del _requests[current_thread()]
        return response
