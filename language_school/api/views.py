from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


from .serializers import ProductSerializer
from api.exceptions import (
    AllGroupsFullError,
    EmptyGroupListError,
    ObjectNotFoundError,
    UserAlreadyInProductError
)
from products.models import Product
from users.models import CustomUser

User = get_user_model()


def distribute_students(objects: list, target: CustomUser, limit: int) -> None:
    """Find suitable group for the user and allocate her to the group.

    Args:
        objects (list): canditate groups
        target (CustomUser): new user
        limit (int): maximum allowed number of students in a group
    """
    counter = 0
    length = objects.count()
    while counter + 1 <= length:
        # if a current group is full notch up the counter
        if objects[counter].students.count() == limit:
            counter += 1
            continue
        # if the current group is last assign a student to it
        if counter + 1 == length:
            objects[counter].students.add(target)
            return
        # if number of students in the current group higher than in the
        # next one notch up the counter
        if (
            objects[counter].students.count() -
            objects[counter + 1].students.count() > 0
        ):
            counter += 1
            continue
        # if all the previous checks failed we can safely assign a student
        # to a current group
        else:
            objects[counter].students.add(target)
            return
    raise AllGroupsFullError(
        "There is not any place left in groups for a new student"
    )

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    http_method_names = ('get', 'post')

    @action(detail=True, methods=["post"])
    def grant(self, request, pk=None) -> Response:
        """Grant access and distribute a user between groups.

        Args:
            request (django request): request object
            pk (str, optional): products id. Defaults to None.

        Raises:
            UserNotFoundError: if given id don't match any user
            ProductNorFoundError: id given id don't match any product

        Returns:
            Response: response object
        """
        try:
            user = User.objects.get(id=request.data.get("user"))
            product = Product.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise ObjectNotFoundError(
                "Either the user or product doesn't exist."
            )
        if user in product.participants.all():
            raise UserAlreadyInProductError(
                "User already has access to the product."
            )
        product.participants.add(user)
        groups = product.groups.all()
        if groups.count() < 1:
            raise EmptyGroupListError(
                (
                    "Product doesn't seem to have any associated groups. "
                    "Add at least one group, please."
                )
            )
        distribute_students(groups, user, product.max_students)

        return Response("Success", status=status.HTTP_200_OK)
