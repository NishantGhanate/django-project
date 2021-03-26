import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.versioning import NamespaceVersioning

from django_project.utils import custom_exceptions as ce
from django_project.common import messages as glob_messages
from django_project.settings import (
    SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SECURE
)

logger = logging.getLogger('testapi')

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class TestCookieView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    versioning_class = VersioningConfig

    def get(self,request):
        try:
            if request.version == 'v1':
                response =  Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK ,
                    'message': 'Testing cookies what',
                    'data': None,
                    }, status = status.HTTP_200_OK)

                response.set_cookie(
                    'get-test-cookie', 'tokens ohho ',
                    httponly=SESSION_COOKIE_HTTPONLY,
                    
                )
                # Only on https
                # response.set_cookie(
                #     'secure-cookie', 'hiibrishString',
                #     secure=SESSION_COOKIE_SECURE
                # )    
                return response
            else:
                raise ce.VersionNotSupported

        
        except ce.ValidationFailed as vf:
            logger.error('TEST COKKIE API VIEW : {}'.format(vf))
            raise

        except ce.VersionNotSupported as vns:
            logger.error('TEST COKKIE API VIEW : {}'.format(vns))
            raise
        
        except Exception as e:
            logger.error(
                'TEST COKKIE API VIEW : {}'.format(e)
            )
            raise ce.InternalServerError

    def post(self,request):
        try:
            if request.version == "v1":

                data = request.data
                response =  Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK ,
                    'message': 'Testing http only cookie via post' ,
                    'data': data,
                    }, status = status.HTTP_200_OK)
                
                # default expiry is session
                response.set_cookie(
                    'post_cookie',
                    'post cookie value',
                    httponly=SESSION_COOKIE_HTTPONLY  
                )
                return response

            else:
                raise ce.VersionNotSupported
        except ce.ValidationFailed as vf:
            logger.error('TEST COKKIE API VIEW : {}'.format(vf))
            raise

        except ce.VersionNotSupported as vns:
            logger.error('TEST COKKIE API VIEW : {}'.format(vns))
            raise
        
        except Exception as e:
            logger.error(
                'TEST COKKIE API VIEW : {}'.format(e)
            )
            raise ce.InternalServerError
