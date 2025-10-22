from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from rest_framework.routers import DefaultRouter
from estabelecimentos.views import EstabelecimentoViewSet


router = DefaultRouter()

# O router irá criar as rotas: /api/estabelecimentos/ e /api/estabelecimentos/<pk>/
router.register(r'estabelecimentos', EstabelecimentoViewSet, basename='estabelecimento')

urlpatterns = [
    path("admin/", admin.site.urls),
    # Endpoints para Autenticação JWT
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),

    path("api/", include("usuarios.urls")),
    path("api/", include(router.urls)),
]
