from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from base.api.permissions import IsAdmin
from base.api.permissions import IsAuthenticated
from base.api.serializers import OperationTypeSerializer

from base.models import OperationType
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    operation_description="get the list operation types ",
    method='get',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOperationType(request):
    operationTypes = OperationType.objects.all()
    serializer = OperationTypeSerializer(operationTypes, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    operation_description="get a detail about an operation type",
    method='get',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDetailedOperationType(request, pk):
    operationTypes = OperationType.objects.get(id=pk)
    serializer = OperationTypeSerializer(operationTypes)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    operation_description="add an operation type",
    method='post',
    request_body=OperationTypeSerializer,
)
@api_view(['POST'])
@permission_classes([IsAdmin])
def addOperationType(request):
    operationType = OperationTypeSerializer(data=request.data)

    if operationType.is_valid():
        operationType.save(createdBy=request.user)
        return Response(operationType.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': operationType.errors}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Update an operation type given ID",
    method='put',
    request_body=OperationTypeSerializer,
)
@api_view(['PUT'])
@permission_classes([IsAdmin])
def updateOperationType(request, pk):
    try:
        operationType = OperationType.objects.get(pk=pk)
    except OperationType.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = OperationTypeSerializer(operationType, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Delete an operation type by ID",
    method='delete',
)
@api_view(['DELETE'])
@permission_classes([IsAdmin])
def deleteOperationType(request, pk):
    try:
        operationType = get_object_or_404(OperationType, pk=pk)
        operationType.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
