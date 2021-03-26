import logging
import datetime
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from testapi.serializers import UserSigninSerializer
from django_project.utils import custom_exceptions as ce

from django_project.settings import (
    SESSION_COOKIE_HTTPONLY, REFRESH_TOKEN_LIFETIME
)

from testapi.models import CustomUser

logger = logging.getLogger('testapi')

class SigninView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserSigninSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({
                    'success': False,
                    'status_code': status.HTTP_401_UNAUTHORIZED ,
                    'message': 'Authentication failed ',
                    'data': serializer.errors,
                }, status = status.HTTP_401_UNAUTHORIZED )

        # TODO : generate jwt token & send it in httpOnly cookie
        max_age = 7*24*60*60
        expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        response = Response({
                'success' : True,
                'status_code' : status.HTTP_200_OK,
                'message': 'User signed in  successfully',
                'data' : None,
            }, status = status.HTTP_200_OK)
        
        response.set_cookie(
            'access',
            serializer.data.get('access'),
            httponly= SESSION_COOKIE_HTTPONLY
        )

        response.set_cookie(
            'refresh',
            serializer.data.get('refresh'),
            httponly= SESSION_COOKIE_HTTPONLY,
            expires= expires,
            
        )

        return response
