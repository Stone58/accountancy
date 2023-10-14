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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # adding custom fields I wanna have inside my token
        token['username'] = user.username
        # token['role'] = user.user_permissions

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@swagger_auto_schema(
    operation_description="get a group list",
    method='get',
)
@api_view(['GET'])
def getGroup(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    operation_description="get a user list",
    method='get',
)
@api_view(['GET'])
@permission_classes([IsAdmin])
def getUser(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    operation_description="get a detail about a user",
    method='get',
)
@api_view(['GET'])
@permission_classes([IsAdmin])
def getDetailedUser(request, pk):
    users = User.objects.get(id=pk)
    serializer = UserSerializer(users)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=['post'],
    request_body=UserSerializer,
    operation_description="Function to add user."
)
@api_view(['POST'])
@permission_classes([IsAdmin])
def addUser(request):
    userData = request.data

    existingUserName = User.objects.filter(
        username=userData.get('username')).first()
    if existingUserName:
        return Response({'message': 'User already exists with the same username.'}, status=status.HTTP_409_CONFLICT)

    user = UserSerializer(data=userData)

    if user.is_valid():
        group = userData.get('group')
        if group and len(group) > 0:
            try:
                group = Group.objects.get(id=group[0])
                user = user.create(user.validated_data)
                user.set_password(userData.get('password'))
                user.save()
                group.user_set.add(user)
            except:
                return Response({'message': 'The group provided not valid'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserSerializer(User.objects.get(id=user.id)).data, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': user.errors}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Update a user informations",
    method='put',
    request_body=UserUpdateSerializer,
)
@api_view(['PUT'])
@permission_classes([IsAdmin])
def updateUser(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserUpdateSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Update a user group",
    method='put',
)
@api_view(['PUT'])
@permission_classes([IsAdmin])
def updateUserGroup(request, pk, pkgroup):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        user.groups.clear()
        user.groups.add(pkgroup)
        return Response({'message': 'User group updated successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Failed to update user's group"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="reset user password",
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_STRING,
        description="New password ",
    ),
)
@api_view(['PUT'])
@permission_classes([IsAdmin])
def updateUserPassword(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({"error": "New password is required in the request body"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'User password updated successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Failed to update user's password"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Delete a user by ID",
    method='delete',
)
@api_view(['DELETE'])
@permission_classes([IsAdmin])
def deleteUser(request, pk):
    try:
        user = get_object_or_404(User, pk=pk)
        if user.username == 'admin':
            return Response({'message': 'you cannot delete the admin account'}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response({'errors': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
