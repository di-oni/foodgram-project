from rest_framework import mixins, viewsets


class CreateDeleteViewSet(viewsets.GenericViewSet,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin):
    """ Пользовательский ViewSet, наследующий GenericViewSet 
        и позволяющий создавать и удалять объекты модели """
    pass
