"""kpi_dyn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from sai.views import SaiViewSet
from bearer.views import BearerViewSet
from pdp.views import PdpViewSet
from globalP import views



# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'sai', SaiViewSet)
router.register(r'bearer', BearerViewSet)
router.register(r'pdp', PdpViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', include('sai.urls')),
    path('sai/attempssai/<target_id>/', SaiViewSet.as_view({"get": "getattemps"})),
    path('', include('bearer.urls')),
    path('', include('uploadFile.urls')),
    path('countries/', views.countryFunctionView, name='country'),
    path('homestats/', views.homedataFunctionView, name='home_stats'),

]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)