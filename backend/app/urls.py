"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .api import api
from django.http import JsonResponse
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
try:
    from wagtail_headless_preview import urls as headless_preview_urls
except Exception:
    # Some versions of wagtail-headless-preview don't expose a `urls` module.
    # Guard against import errors so the project can run without that submodule.
    headless_preview_urls = None


@csrf_exempt
@require_http_methods(["GET", "HEAD"])
def health_check(request):
    """
    Health check endpoint for load balancers and monitoring.
    Returns 200 OK with minimal response to confirm service is running.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # Log health check details for debugging
    host = request.META.get('HTTP_HOST', 'NONE')
    logger.debug(f"Health check from Host: {host}")
    
    return JsonResponse({'status': 'ok'}, status=200)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    # Include headless preview URLs only if the package exposes them
    path("schema-viewer/", include("schema_viewer.urls")), 
    path('accounts/', include('accounts.urls')),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
    path('health/', health_check, name='health_check'),
]
if headless_preview_urls:
    urlpatterns.insert(2, path("headless-preview/", include(headless_preview_urls)))

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )
