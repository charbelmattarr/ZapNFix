from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50)
    number = models.CharField(max_length=15)
    location = models.CharField(max_length=100)

class Repair(models.Model):
    desc = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    repairDate = models.DateField(null=True, blank=True)
    actualRepairDate = models.DateField(null=True, blank=True)
    pricing = models.DecimalField(max_digits=8, decimal_places=2)
    isDelivery = models.BooleanField(default=False)
    image = models.ImageField(upload_to='repair_images/', null=True, blank=True)
    feedbackRate = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    product_id = models.ForeignKey('Brand', on_delete=models.CASCADE)
    user_idClient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repairs_client')
    user_idTech = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repairs_technician')

class Brand(models.Model):
    desc = models.CharField(max_length=50)
    type_id = models.ForeignKey('Type', on_delete=models.CASCADE)

class Type(models.Model):
    desc = models.CharField(max_length=50)

class Component(models.Model):
    desc = models.CharField(max_length=50)

class Problem(models.Model):
    desc = models.CharField(max_length=100)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)
    component_id = models.ForeignKey(Component, on_delete=models.CASCADE)


