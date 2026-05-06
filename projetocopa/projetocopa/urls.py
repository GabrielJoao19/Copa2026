"""
URL configuration for projetocopa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from rest_framework import routers
from copa26 import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r'selecoes', views.SelecaoViewSet)
router.register(r'jogadores', views.JogadorViewSet)
router.register(r'jogos', views.JogoViewSet)
router.register(r'tecnicos', views.TecnicoViewSet)
router.register(r'grupos', views.GrupoViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Copa 2026 API",
        default_version='v1',
        description="API da Copa 2026",
    ),
    public=True,
    permission_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0))
]
