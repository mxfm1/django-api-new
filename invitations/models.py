from django.db import models
import uuid
from houses.models import Residence
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Invitation(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=120, unique=True, editable=False)
    guest_name= models.CharField(max_length=120)
    reason = models.CharField(max_length=120)
    valid_until = models.DateTimeField()
    aditional_information = models.TextField(max_length=250,null=True,blank=True)

    residence = models.ForeignKey(Residence,on_delete=models.CASCADE)
    host = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.valid_until
    
    def save(self,*args,**kwarsg):
        if not self.code:
            self.code = uuid.uuid4().hex[:8].upper()
        super().save(*args,**kwarsg)
