from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ecart(models.Model):
  
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    name=models.CharField(max_length=200,unique=True)
    picture=models.ImageField(upload_to="images",null=True)
    price=models.FloatField()


    def __str__(self):
        return self.name
    


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ecart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.BooleanField(default=False) 
    added_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"


    
class UserProfile(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    password=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
   

    

