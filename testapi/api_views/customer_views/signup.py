import json
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.versioning import NamespaceVersioning
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from testapi.serializers import UserCreateSerializer

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django_project.utils.token_generator import account_activation_token

from django.utils.encoding import(
    force_bytes, force_text
)
from django.utils.http import (
    urlsafe_base64_encode, urlsafe_base64_decode
)
from django_project.settings import EMAIL_HOST_USER
from django_project.common import messages 
from django_project.utils import custom_exceptions as ce

logger = logging.getLogger('testapi')

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class SignUpApiView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    versioning_class = VersioningConfig

    def post(self, request):

        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() 
            # logger.info(
            #     "SignupView - user type = {}".format(type(user))
            # )
            # logger.info(user._meta.get_fields())
            
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                    'success': True,
                    'status_code': status.HTTP_201_CREATED ,
                    'message': 'User created sucessefully ',
                    'data': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'redirect_url' : 'https://127.0.0.1/v1/auth/sign-in',
                    },
                }, status = status.HTTP_201_CREATED )
        else:
            return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST ,
                    'message': 'Something went wrong',
                    'data': {
                        'errors': serializer.errors.mes,
                    },
                }, status = status.HTTP_400_BAD_REQUEST )

class SignUpVerifyView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    versioning_class = VersioningConfig
    
    def post(self,request):
        try:
            if request.version == 'v1':
                serializer = UserCreateSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response({
                            'success': False,
                            'status_code': status.HTTP_400_BAD_REQUEST ,
                            'message': messages.VALIDATION_FAILED,
                            'data': serializer.errors ,
                        }, status = status.HTTP_400_BAD_REQUEST )

                user = serializer.save() 
                # Here it shouuld be front end path and it makes api call 
                # on activation link 
                current_site = get_current_site(request)
                to_email = user.email
                email_subject = messages.ACTIVATE_ACCOUNT
                context = {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    }
                html_content = render_to_string('verify_email.html', context)
                text_content =''
                msg = EmailMultiAlternatives(
                        email_subject, 
                        text_content,
                        EMAIL_HOST_USER, 
                        [to_email]
                    )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                return Response({
                        'success': True,
                        'status_code': status.HTTP_200_OK ,
                        'message': messages.SEND_ACTIVATION_LINK,
                        'data': None,
                    }, status = status.HTTP_200_OK )
               
                    
            else:
                raise ce.VersionNotSupported
        except ce.ValidationFailed as vf:
            logger.error('SIGN UP VERIFY API VIEW : {}'.format(vf))
            raise

        except ce.VersionNotSupported as vns:
            logger.error('SIGN UP VERIFY API VIEW : {}'.format(vns))
            raise
        
        except Exception as e:
            logger.error(
                'SIGN UP VERIFY API VIEW : {}'.format(e)
            )
            raise ce.InternalServerError

class ActivateUserView(APIView):

    def get(self,request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
           
            return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK ,
                    'message': messages.EMAIL_CONFIRMED,
                    'data': None,
                }, status = status.HTTP_200_OK )
        else:
            message = 'Activation link is invalid'
            return Response({
                    'success': False,
                    'status_code': status.HTTP_200_OK ,
                    'message': messages.INVALID_ACTIVATION_LINK,
                    'data': None,
                }, status = status.HTTP_200_OK )