from rest_framework import status
from rest_framework.response import Response


class CreateDeleteObjMixin:
    '''Mixin for adding sample recipe-related create/delete methods.'''

    def create_obj(self, instance, serializer, request):
        serializer = serializer(
            data={
                'user': request.user.id,
                'recipe': instance.id,
            },
            context={
                'request': request
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, instance, model, request, error):
        if model.objects.filter(user=request.user, recipe=instance).exists():
            model.objects.filter(user=request.user, recipe=instance).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': error, },
            status=status.HTTP_400_BAD_REQUEST
        )
