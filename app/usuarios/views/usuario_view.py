from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..serializers import (
    ChangePasswordSerializer,
)


import logging

logger = logging.getLogger("app")

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(
                "Senha alterada para o usuário: %s",
                self.object.email
            )
            return Response(
                {"detail": "Senha alterada com sucesso."}, status=status.HTTP_200_OK
            )

        logger.error(
            "Erro ao alterar senha para o usuário: %s",
            self.object.email
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
