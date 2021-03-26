from rest_framework.permissions import ( 
    AllowAny, IsAuthenticated, IsAdminUser
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.versioning import NamespaceVersioning


class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class HelloApiView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    versioning_class = VersioningConfig

    def get(self, request):
        return Response({
                'success': True,
                'status_code': status.HTTP_200_OK ,
                'message': 'Thank you',
                'data': 'Hello boi, ',
            }, status = status.HTTP_200_OK )

class HelloCustomerView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    versioning_class = VersioningConfig

    def get(self, request):
        return Response({
                'success': True,
                'status_code': status.HTTP_200_OK ,
                'message': 'Thank you  for your token',
                'data': 'Hello Customer, ',
            }, status = status.HTTP_200_OK )



