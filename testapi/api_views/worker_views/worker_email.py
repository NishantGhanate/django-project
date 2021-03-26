from rest_framework.permissions import ( 
    AllowAny
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.versioning import NamespaceVersioning
from testapi.serializers import EmailSerializer
from testapi.tasks import send_worker_email_task

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class WorkerEmail(APIView):
    permission_classes = [AllowAny]
    versioning_class = VersioningConfig
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({
                    'success': False,
                    'status_code': '' ,
                    'message': 'Validation failed',
                    'data': serializer.errors,
                }, status = status.HTTP_401_UNAUTHORIZED )

        # TODO : send woker email , return http response
        send_worker_email_task.delay(serializer.data)
        return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK ,
                    'message': 'Email sent',
                    'data': serializer.data,
                }, status = status.HTTP_200_OK )