from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from products.models import Lesson, Product

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

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        exclude = ("product",)


class RetrieveSerializer(ProductSerializer):
    """Serializer for retrieving a single product.

    With corresponding lessons.
    """
    lessons = serializers.SerializerMethodField()

    @extend_schema_field(field=LessonSerializer(many=True))
    def get_lessons(self, obj):
        queryset = obj.lessons.filter(
            product__participants__id=self.context.get("request").user.id
        )
        return LessonSerializer(queryset, many=True).data
