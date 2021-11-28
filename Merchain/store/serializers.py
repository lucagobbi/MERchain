from .models import Product
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'user', 'date_added', 'price', 'deadline', 'winner', 'lastBid']
