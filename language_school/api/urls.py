from rest_framework import routers

from .views import ProductViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')

urlpatterns = router.urls
