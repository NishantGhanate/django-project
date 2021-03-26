import json
import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.versioning import NamespaceVersioning

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from django_project.settings import EMAIL_HOST_USER
from django_project.utils import custom_exceptions as ce
from django_project.utils.custom_validators import CustomValidator
from django_project.common import messages as glob_messages

logger = logging.getLogger('testapi')

# Get an instance of custom Validator
c_validator = CustomValidator({}, allow_unknown = True)

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class TestEmailView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    versioning_class = VersioningConfig

    def post(self,request):
        try:
            if request.version == 'v1':

                schema = {
                    'username':{
                        'required': True,
                        'isalphanumeric': True
                    },
                    'email':{
                        'required': True,
                        'isemail' : True
                    }
                }
            
                is_valid = c_validator.validate(
                    request.data, schema
                )
                if not is_valid:
                    raise ce.ValidationFailed({
                        'message': glob_messages.VALIDATION_FAILED,
                        'data': c_validator.errors
                    })

                
                return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK ,
                    'message': 'Email sent ;) ',
                    'data': None,
                    }, status = status.HTTP_200_OK)

            else:
                raise ce.VersionNotSupported

        except ce.ValidationFailed as vf:
            logger.error('TEST EMAIL API VIEW : {}'.format(vf))
            raise

        except ce.VersionNotSupported as vns:
            logger.error('TEST EMAIL API VIEW : {}'.format(vns))
            raise
        
        except Exception as e:
            logger.error(
                'TEST EMAIL API VIEW : {}'.format(e)
            )
            raise ce.InternalServerError

