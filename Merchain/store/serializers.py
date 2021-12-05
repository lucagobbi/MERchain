from .models import Product
from rest_framework import serializers

# serialize details about the auction

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'user', 'date_added', 'price', 'deadline', 'winner', 'last_bid']
