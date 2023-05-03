from django.db import models

# Create your models here.
class vehicleModel(models.Model):
    model_id = models.AutoField(primary_key=True, db_column='id')
    
    vendor = models.CharField(max_length=20,null=False,blank=False)
    
    model = models.CharField(max_length=20 , null=False,blank=False, default='unKnown')
    
    type = models.CharField(max_length=50,choices=[(t.name,t.value) for t in
    