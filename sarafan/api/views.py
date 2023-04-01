from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.models import Category, Product, ProductCart

from .serializers import (CartSerializer, CategorySerializer,
                          ProductCartSerializer, ProductSerializer)
from .viewsets import ListModelViewSet, UpdateModelViewSet


class CategoryViewSet(ListModelViewSet):
    queryset = Category.objects.prefetch_related('sub_categories')
    serializer_class = CategorySerializer


class ProductViewSet(ListModelViewSet):
    queryset = Product.objects.select_related('sub_category__category')
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    @action(
        methods=('post',),
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def to_cart(self, request, slug):
        user = request.user
        product = self.get_object()
        cart_unit, create = ProductCart.objects.get_or_create(
            product=product,
            user=user,
        )
        if not create:
            cart_unit.amount += 1
        cart_unit.save()
        return Response(
            self.get_serializer(product).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=('delete',),
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def from_cart(self, request, slug):
        user = request.user
        product = self.get_object()
        get_object_or_404(ProductCart, product=product, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartUpdateViewSet(UpdateModelViewSet):
    queryset = ProductCart.objects
    serializer_class = ProductCartSerializer
    permission_classes = (IsAuthenticated,)

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=CartSerializer,
    )
    def get(self, request):
        return Response(
            self.get_serializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    @action(
        methods=('put',),
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=CartSerializer,
    )
    def clear(self, request):
        request.user.m2m_product.all().delete()
        return Response(
            self.get_serializer(request.user).data,
            status=status.HTTP_200_OK,
        )
