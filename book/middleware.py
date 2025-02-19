import time
from django.utils.deprecation import MiddlewareMixin

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - request.start_time
        print(f"Request: {request.method} {request.path} - Params: {request.GET} - Duration: {duration}s")
        return response