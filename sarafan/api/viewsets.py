from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet


class ListModelViewSet(GenericViewSet, ListModelMixin):
    pass


class UpdateModelViewSet(GenericViewSet, UpdateModelMixin):
    pass
