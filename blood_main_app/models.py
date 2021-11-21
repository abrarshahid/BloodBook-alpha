from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    location = models.CharField(max_length=1800)
    role = models.CharField(max_length=50)
    blood_grp = models.CharField(max_length=10)
    served = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=13)
    service_type = models.CharField(max_length=90,default="volunteer")
    neighbourhood = models.CharField(max_length=300,default=" ")
    town = models.CharField(max_length=300,default=" ")
    img =  models.ImageField(upload_to='images/')
    deactivated_time = models.DateField(null=True)
class Compliment(models.Model):
    compliment_id = models.AutoField(primary_key=True)
    compliment = models.CharField(max_length=200)
    complimenter = models.ForeignKey(User,on_delete=models.CASCADE,related_name="complimenter")
    complimented_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name="complimented")
    def __str__(self):
        return self.compliment

class p2p_donation_receive(models.Model):
    log_id = models.AutoField(primary_key=True)
    donor = models.ForeignKey(User,on_delete=models.CASCADE,related_name="donor")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")
    status = models.CharField(max_length=90)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.donor} gave blood to {self.receiver}"

class emergency_receiver(models.Model):
    receiver_id = models.AutoField(primary_key=True)
    emergency_receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="emergency_receiver")
    neighbourhood = models.CharField(max_length=300,default=" ")
    town = models.CharField(max_length=300,default=" ")
    location = models.CharField(max_length=1800,default=" ")
    blood_grp = models.CharField(max_length=20,default=" ")
    status = models.CharField(max_length=90,default="requested")
    emergency_donor =  models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="emergency_donor")

    def __str__(self):
        return f"{self.emergency_receiver} needs blood!"