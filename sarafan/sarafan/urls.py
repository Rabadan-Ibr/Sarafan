from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
      title="Store API",
      default_version='v1',
      description="Test task",
    ),
    public=True,
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    re_path(
        r'^docs(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
