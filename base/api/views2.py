from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from base.api.permissions import IsAdmin
from base.api.permissions import IsAuthenticated
from base.api.serializers import CompanySerializer, GroupSerializer, OperationSerializer, OperationTypeSerializer, OperationUpdateSerializer, UserSerializer, UserUpdateSerializer

from base.models import Operation, OperationType, Company
from django.contrib.auth.models import User, Group
from rest_framework import status
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    operation_description="get the list of all endpoint of the api ",
    method='get',
)
@api_view(['GET'])
def getRoutes(request):
    routes = {
        "Authentication": [
            '/api/token',
            '/api/toke/refresh'],
        "users":  {
            'list': '/list',
            'Add': '/create',
            'Update': '/update/pk',
            'Delete': '/delete/pk',
            'update user group': 'user/updategroup/<int:pk>/<int:pkgroup>',
            'update password': 'user/updatepassword/<int:pk>'},
        "operation":  {
            'list': '/list',
            'Add': '/create',
            'Update': '/update/pk',
            'Delete': '/delete/pk'},
        "Company":  {
            'list': '/list',
            'Add': '/create',
            'Update': '/update/pk',
            'Delete': '/delete/pk'},
        "user":  {
            'list': '/list',
            'Add': '/create',
            'Update': '/update/pk',
            'Delete': '/delete/pk'},
        "groups":  {
            'list': '/list',
            'Add': '/create',
            'Update': '/update/pk',
            'Delete': '/delete/pk'}
    }

    return Response(routes)



