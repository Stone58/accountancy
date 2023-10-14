from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q

from base.api.permissions import IsAuthenticated
from base.api.serializers import OperationSerializer, OperationUpdateSerializer

from base.models import Operation
from rest_framework import status
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema


@api_view(['GET'])
def getOperationOverview(request):
    routes = {
        'list': '/api/operation/list',
        'list a detail': '/api/operation/list/<int:pk>',
        'Add': '/api/operation/create',
        'Update': '/api/operation/update/<int:pk>',
        'Delete': '/api/operation/delete/<int:pk>'
    }

    return Response(routes)


@swagger_auto_schema(
    operation_description="get the list operation",
    method='get',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOperation(request):
    user_groups = request.user.groups.all()
    if user_groups.filter(Q(name='Admin') | Q(name='Accountant')).exists():
        operations = Operation.objects.all()
    else:
        operations = Operation.objects.filter(createdBy_id=request.user.id)
    serializer = OperationSerializer(operations, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    operation_description="get a detail about an operation",
    method='get',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDetailedOperation(request, pk):
    user_groups = request.user.groups.all()

    try:
        if user_groups.filter(Q(name='Admin') | Q(name='Accountant')).exists():
            operations = Operation.objects.get(id=pk)
        else:
            operations = Operation.objects.get(
                Q(id=pk) & Q(createdBy_id=request.user.id))
    except ObjectDoesNotExist:
        return Response({'message': 'Operation not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OperationSerializer(operations)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    operation_description="add an operation",
    method='post',
    request_body=OperationSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOperation(request):
    operation = OperationSerializer(data=request.data, partial=True)

    if operation.is_valid():
        operation.save(createdBy=request.user,
                       operationDate=timezone.now().isoformat())
        return Response(operation.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': operation.errors}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Update an operation given ID",
    method='put',
    request_body=OperationSerializer,
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOperation(request, pk):
    try:
        operation = Operation.objects.get(pk=pk)
    except operation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = OperationUpdateSerializer(operation, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Delete an operation by ID",
    method='delete',
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteOperation(request, pk):
    try:
        operation = get_object_or_404(Operation, pk=pk)
        operation.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
