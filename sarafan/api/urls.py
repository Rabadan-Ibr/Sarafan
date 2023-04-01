from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CartUpdateViewSet, CategoryViewSet, ProductViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('category', CategoryViewSet)
router_v1.register('product', ProductViewSet)
router_v1.register('cart', CartUpdateViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
