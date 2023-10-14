from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# TODO : create a to string method for every model

# for user management, create a custom user model to that store username, password, role


class Task(models.Model):
    class Meta:
        permissions = [

            ('Admin', 'Admin'),  # for admin roles
            ('Accountant', 'Accountant'),  # for Muhasebeci:
            ('Worker', 'Worker'),  # for işlemci
        ]


"""
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),  # for admin roles
        ('Accountant', 'Accountant'),  # for Muhasebeci:
        ('Worker', 'Worker'),  # for işlemci
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
"""


class OperationType(models.Model):
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    operationType = models.CharField(max_length=200, unique=True)

class Company(models.Model):
    # we cannot put on delete cascade in here because even if a user is deleted(that is not supposed to happen, disable option is more convenient) the companies should still exists
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=100, unique=True, null=False)
    taxNumber = models.IntegerField(unique=True, null=False)
    address = models.CharField(max_length=200)


class Operation(models.Model):
    # we cannot put on delete cascade in here because even if a user is deleted(that is not supposed to happen, disable option is more convenient) the operation should still exists
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    operationType = models.ForeignKey(OperationType, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=5)
    operationDate = models.DateTimeField()


    '''def __str__(self) -> str:
            return self.name'''

# Create your models here.
