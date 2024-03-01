from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import ProductSerializer
from products.models import Product

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @action(detail=True, methods=["post"])
    def grant(self, request, pk=None):
        return Response("Success", status=status.HTTP_200_OK)
