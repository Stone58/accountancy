from django.urls import path
from . import views
from .views2 import getRoutes
from .views import company, operationType, operation, user

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib.auth.models import User, Group

# init create groups
adminGroup, created = Group.objects.get_or_create(name='Admin')
Group.objects.get_or_create(name='Accountant')
Group.objects.get_or_create(name='Worker')

# set admin to admin group
adminUser, created = User.objects.get_or_create(username='admin', defaults={
                                                "password": '1234', "email": 'admin@admin.com', "is_active": True, "is_staff": True, "is_superuser": True})
if created:
    adminUser.set_password('1234')
    adminUser.save()

adminGroup.user_set.add(adminUser)

urlpatterns = [
    path('', getRoutes),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #    path('operation-type/list', views.getOperationType),

    # path('group', views.groupOverview),

    path('operationtype/list', operationType.getOperationType),
    path('operationtype/list/<int:pk>', operationType.getDetailedOperationType),
    path('operationtype/create', operationType.addOperationType),
    path('operationtype/update/<int:pk>', operationType.updateOperationType),
    path('operationtype/delete/<int:pk>', operationType.deleteOperationType),

    path('operation', operation.getOperationOverview),
    path('islemler', operation.getOperationOverview),
    path('operation/list', operation.getOperation),
    path('operation/list/<int:pk>', operation.getDetailedOperation),
    path('operation/create', operation.addOperation),
    path('operation/update/<int:pk>', operation.updateOperation),
    path('operation/delete/<int:pk>', operation.deleteOperation),

    path('company', company.getCompanyOverview),
    path('firmalar', company.getCompanyOverview),
    path('company/list', company.getCompany),
    path('company/list/<int:pk>', company.getDetailedCompany),
    path('company/create', company.addCompany),
    path('company/update/<int:pk>', company.updateCompany),
    path('company/delete/<int:pk>', company.deleteCompany),

    path('token/', user.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('user/list', user.getUser),
    path('user/list/<int:pk>', user.getDetailedUser),
    path('user/create', user.addUser),
    path('user/updategroup/<int:pk>/<int:pkgroup>', user.updateUserGroup),
    path('user/updatepassword/<int:pk>', user.updateUserPassword),
    path('user/update/<int:pk>', user.updateUser),
    path('user/delete/<int:pk>', user.deleteUser),
    path('group/list', user.getGroup),
]

