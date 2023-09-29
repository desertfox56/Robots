from django.db import models
from customers.models import Customer
from robots.models import Robot
from customers.models import Customer

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='customer_order')
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE,related_name='robot_order',null=True)

class WaitlistOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_waitlist_order',null=True)
    model = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    is_backordered = models.BooleanField()