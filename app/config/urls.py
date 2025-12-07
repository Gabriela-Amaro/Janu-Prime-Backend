from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from rest_framework.routers import DefaultRouter
from estabelecimentos.views import EstabelecimentoViewSet
from produtos.views import ProdutoViewSet
from anuncios.views import AnuncioViewSet
from fotos_espaco.views import FotosEspacoViewSet
from avaliacoes.views import AvaliacaoPlataformaViewSet, AvaliacaoEstabelecimentoViewSet


router = DefaultRouter()

router.register(r"estabelecimentos", EstabelecimentoViewSet, basename="estabelecimento")
router.register(r"produtos", ProdutoViewSet, basename="produto")
router.register(r"anuncios", AnuncioViewSet, basename="anuncio")
router.register(r"fotos-espaco", FotosEspacoViewSet, basename="fotos_espaco")
router.register(
    r"avaliacoes/plataforma",
    AvaliacaoPlataformaViewSet,
    basename="avaliacao_plataforma",
)
router.register(
    r"avaliacoes/estabelecimento",
    AvaliacaoEstabelecimentoViewSet,
    basename="avaliacao_estabelecimento",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Endpoints para Autenticação JWT
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("api/", include("usuarios.urls")),
    path("api/", include(router.urls)),
]
