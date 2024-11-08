from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.

class UserPreferences(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE)       
    currency = models.CharField(max_length=255,blank=True,null=True)
    # instance variables are accessed using self. 

    def __str__(self):
        return str(self.user)+"'s"+' preferences'