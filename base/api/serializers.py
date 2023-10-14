from rest_framework.serializers import ModelSerializer
from base.models import Operation, OperationType, Company
from django.contrib.auth.models import User, Group


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'createdBy_id', 'companyName', 'taxNumber', 'address']


class OperationSerializer(ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'

class OperationUpdateSerializer(ModelSerializer):
    class Meta:
        model = Operation
        fields = ['quantity', 'company', 'operationType']

class OperationTypeSerializer(ModelSerializer):
    class Meta:
        model = OperationType
        fields = ['id', 'operationType']
