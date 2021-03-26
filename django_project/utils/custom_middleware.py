# https://docs.djangoproject.com/en/3.1/topics/http/middleware/#writing-your-own-middleware

import json

class BaseMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
        

class CookieToBodyMiddlware(BaseMiddleware):
               
    def process_view(self, request, view_func, view_args, view_kwargs):
        # print('----- Middleware view %s ----------' % view_func.__name__)
        # print('----- Request path %s ----------'% request.path )

        if request.path == '/v1/testapi/test-cookie' and request.method == 'POST':
            data = json.loads(request.body)
            data['token'] = request.COOKIES.get('token')
            # print(data)
            
            request._body = json.dumps(data).encode('utf-8')
            # print(type(request._body))
        return None