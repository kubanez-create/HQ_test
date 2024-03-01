from rest_framework import serializers

from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Product serializer"""
    lessons = serializers.StringRelatedField(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "start_time",
            "cost",
            "author",
            "lessons",
        )