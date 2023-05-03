from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models

from baham.constants import COLOURS, TOWNS
from baham.enum_types import VehicleType, Vehiclestatus, UserType
# Custom validators.
def validate_colour (value):
    ''''
    Validate that the value exists in the list of available colours
    '''
    return value.upper() in COLOURS

# Create your models here.
class VehicleModel (models. Model):
    
    
    model_id = models.AutoField (primary_key=True, db_column='id')
# Toyota, Honda, Suzuki, Kia, etc.
    vendor = models.CharField(max_length=20, null=False, blank=False)
# Corolla, Vitz, City, Sportage, etc.
    model = models.CharField (max_length=20, null=False, blank=False, default='Unknown')
# Sedan, Motorcyle, SUV, Van, etc.
    type = models.CharField(max_length=50, choices=[(t.name, t.value) for t in VehicleType],
help_text="Select the vehicle chassis type")
# Sitting capacity
    capacity = models. PositiveSmallIntegerField(null=False, default=2)
class Meta:
    db_table="baham_vehicle_model"
    
    class Vehicle (models.Model):
        vehicle_id = models.AutoField (primary_key=True, db_column='id')
        # ABC-877
        registration_number= models. CharField (max_length=10, unique=True, null=False, blank=False,
        help_text="Unique registration/license plate no. of the vehicle.")
        colour = models. CharField (max_length=50, default='white', validators= [validate_colour])
        model = models. ForeignKey(VehicleModel, null=False, on_delete=models.CASCADE)
        owner = models. ForeignKey (User, null=False,on_delete=models.CASCADE)
        status = models.CharField (max_length=50, choices=[(t.name, t.value) for t in Vehiclestatus])
        picture1 = models. ImageField (upload_to='pictures', null=True) I
        picture2 = models. ImageField (upload_to='pictures', null=True)
def _str_(self):
    return f"{self.model.vendor} {self.model.model} {self.colour}"

class User (models. Model):
    user_id = models.AutoField (primary_key=True, db_column='id')
    username = models. CharField (max_length=20, unique=True, null=False, blank=False)
    password_hash = models.CharField(max_length=512, null=False, blank=False)
    first_name=models.CharField (max_length=50, null=False, blank=False)
    last_name = models. CharField (max_length=50, null=False, blank=False)
    birthdate= models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    email = models.models.EmailField(_null=False ,blank=False)
    primary_contact = models.CharField (max_length=20, null=False, blank=False)
    alternate_contact = models.CharField (max_length=20, null=True)
    address = models. CharField (max_length=255)
    address_latitude = models.DecimalField (max_digits=9, decimal_places=6, null=True)
    address_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    landmark = models. CharField (max_length=255, null=False)
    town = models. CharField(max_length=50, null=False, choices=[(c, c) for c in TOWNS]) I
    active = models. BooleanField (default=True, editable=False)
    date_deactivated = models.DateTimeField (editable=False, null=True)
    bio = models. TextField()
    
def _str__(self):
    return f"{self.username} {self.first_name} {self.last_name}"

class Owner (User):
    date_joined= models.DateField(null=False)
    active_contracts = models.PositiveSmallIntegerField (default=0)
class Companion (User):
    has_contract = models. BooleanField (default=False, null=False)
    
    
class Contract (models.Model):
    contract_id = models.AutoField (primary_key=True, db_column='id')
    vehicle = models.ForeignKey(Vehicle, null=False, on_delete=models.CASCADE)
    companion = models.ForeignKey(UserProfile, null=False, on_delete=models.CASCADE)
    effective_start_date= models.DateField(null=False)
    expiry_date= models.DateField()
    is_active= models. BooleanField (default=True)
    fuel_share= models. PositiveSmallIntegerField (help_text="Percentage of fuel contribution.")
    maintenance_share = models.PositiveSmallIntegerField (help_text="Percentage of maintenance cost contribution.")
    schedule= models. CharField (max_length=255, null=False)
#Add Audit fields    
class MyModel(models.Model):
    user_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='%(class)s_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated')

class MyChildModel(MyModel):
    description = models.TextField()
    
#Override the delete method and disable it for non-staff members.

class Member(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def delete(self, *args, **kwargs):
        if not kwargs.get('using'):
            self.update(is_deleted=True)
class MyModel(models.Model):
    name = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)

    objects = Member()

    def delete(self, *args, **kwargs):
        if self.pk and not self.is_staff:
            raise PermissionError("Non-staff members cannot delete this object.")
        else:
            super().delete(*args, **kwargs)

