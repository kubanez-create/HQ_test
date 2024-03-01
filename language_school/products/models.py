from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, URLValidator
from django.db import models

from .validators import validate_start_time


User = get_user_model()


class Product(models.Model):
    name = models.CharField("Product name", max_length=200,)
    start_time = models.DateTimeField(
        "Start time",
        validators=[validate_start_time]
    )
    cost = models.FloatField(
        "Cost of a product",
        validators=[
            MinValueValidator(
                limit_value=0,
                message="Cost of a product must be a positive number"
            )
        ]
    )
    author = models.ForeignKey(
        User,
        verbose_name="Author",
        on_delete=models.CASCADE,
        related_name="products",
    )
    max_students = models.PositiveSmallIntegerField(
        "Maximum number of students in a group",
    )
    min_students = models.PositiveSmallIntegerField(
        "Minimum number of students in a group",
        validators=[
            MinValueValidator(
                limit_value=1,
                message="Group can't be less than one person.")
        ]
    )
    participants = models.ManyToManyField(
        User,
        verbose_name="Students",
        related_name="courses",
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_name_start_time_pair',
                fields=['name', 'start_time'],
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} starts at {self.start_time}"


class Lesson(models.Model):
    name = models.CharField("Lesson name", max_length=200,)
    video_link = models.URLField(
        "Video link",
        validators=[
            URLValidator(message="Your link doesn't look like a valid url.")
        ]
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Product",
        on_delete=models.CASCADE,
        related_name="lessons",
    )

    def __str__(self) -> str:
        return self.name


class Group(models.Model):
    name = models.CharField("Group name", max_length=200,)
    product = models.ForeignKey(
        Product,
        verbose_name="Product",
        on_delete=models.CASCADE,
        related_name="groups"
    )
    students = models.ManyToManyField(
        User,
        verbose_name="Students",
        related_name="classes",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name
