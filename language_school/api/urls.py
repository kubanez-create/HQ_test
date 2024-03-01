from django.urls import include, path
from rest_framework import routers

from .views import ProductViewSet  #, LessonViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
# router.register(r'lessons', LessonsViewSet, basename='lessons')

urlpatterns = router.urls
