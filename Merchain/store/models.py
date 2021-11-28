from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers
from .utils import sendTransaction
import hashlib
import json

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='user')
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True, blank=True)
    lastBid = models.FloatField(default=0, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(auto_now_add=False, auto_now=False)
    description = models.CharField(max_length=5000, null=True)
    done = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner', null=True, blank=True)
    image = models.ImageField(upload_to='product_imgs', default='default.png')
    hash = models.CharField(max_length=64, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def writeOnChain(self, serializer):
        serializer.hash = hashlib.sha256(json.dumps(serializer.data).encode('utf-8')).hexdigest()
        self.txId = sendTransaction(serializer.hash)
        self.hash = serializer.hash
        self.save()
    

class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.FloatField()

