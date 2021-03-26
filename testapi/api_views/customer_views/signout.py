import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.versioning import NamespaceVersioning

from django_project.utils import custom_exceptions as ce
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger('testapi')

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class SignOutView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser]
    versioning_class = VersioningConfig

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                'success' : True,
                'status_code' : status.HTTP_200_OK,
                'message': 'User signed out successfully',
                'data' : None,
            },status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            logger.error(
                "SignOutView - {}".format(e)
            )
            raise ce.InternalServerError


class SignOutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)