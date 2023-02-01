from . import models

# This is a custom middleware which send Request object inside models.py.
# to do this, we need to mention "request_object = ''" in models.py
def RequestObjectMiddleware(get_response):
    # One-time configuration and initialization.
    
    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        models.request_object = request

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware