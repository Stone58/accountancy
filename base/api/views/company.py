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
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    operation_description="get a detail about a company api list",
    method='get',
)
@api_view(['GET'])
def getCompanyOverview(request):
    routes = {
        'list': '/api/company/list',
        'list a detail': '/api/company/list/<int:pk>',
        'Add': '/api/company/create',
        'Update': '/api/company/update/<int:pk>',
        'Delete': '/api/company/delete/<int:pk>'
    }

    return Response(routes)


@swagger_auto_schema(
    operation_description="get a detail about a company",
    method='get',
)
@api_view(['GET'])
def getCompany(request):
    companys = Company.objects.all()
    serializer = CompanySerializer(companys, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    operation_description="get a detail about an company",
    method='get',
)
@api_view(['GET'])
def getDetailedCompany(request, pk):
    companys = Company.objects.get(id=pk)
    serializer = CompanySerializer(companys)
    return Response(serializer.data)


@swagger_auto_schema(
    methods=['post'],
    request_body=CompanySerializer,
    operation_description="Function to add company."
)
@api_view(['POST'])
@permission_classes([IsAdmin])
def addCompany(request):
    companyData = request.data

    existingCompanyName = Company.objects.filter(
        companyName=companyData.get('companyName')).first()
    if existingCompanyName:
        return Response({'message': 'Company already exists with the same company name.'}, status=status.HTTP_409_CONFLICT)
    existingCompanyTaxNumber = Company.objects.filter(
        taxNumber=companyData.get('taxNumber')).first()
    if existingCompanyTaxNumber:
        return Response({'message': 'Company already exists with the same tax number.'}, status=status.HTTP_409_CONFLICT)

    company = CompanySerializer(data=request.data)

    if company.is_valid():
        company.save(createdBy=request.user)
        return Response(company.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'The information provided are not valid'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Update a company given ID",
    method='put',
    request_body=CompanySerializer,
)
@api_view(['PUT'])
@permission_classes([IsAdmin])
def updateCompany(request, pk):
    try:
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CompanySerializer(company, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Delete an company by ID",
    method='delete',
)
@api_view(['DELETE'])
@permission_classes([IsAdmin])
def deleteCompany(request, pk):
    try:
        company = get_object_or_404(Company, pk=pk)
        company.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
