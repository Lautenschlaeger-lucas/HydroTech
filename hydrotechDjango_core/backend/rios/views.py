import logging
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Rios, PontoRisco
from .serializers import RiosSerializer, PontoRiscoSerializer
from usuarios.authentication import JWTOrAPITokenAuthentication
from usuarios.permissions import IsDefesaCivilAdminOrOwner

logger = logging.getLogger(__name__)


class RiosListCreateView(generics.ListCreateAPIView):
    serializer_class = RiosSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rios.objects.filter(criado_por=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
        logger.info(f'Novo rio criado: {serializer.instance.nome} por {self.request.user.email}')


class RiosRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiosSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rios.objects.filter(criado_por=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Rio atualizado: {serializer.instance.nome}')

    def perform_destroy(self, instance):
        nome = instance.nome
        instance.delete()
        logger.info(f'Rio deletado: {nome}')


class RiosFavoriteView(APIView):
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            rio = get_object_or_404(Rios, pk=pk, criado_por=request.user)
            
            if request.user.favoritos.filter(pk=rio.pk).exists():
                request.user.favoritos.remove(rio)
                favorito = False
                logger.info(f'Rio removido de favoritos: {rio.nome} por {request.user.email}')
            else:
                request.user.favoritos.add(rio)
                favorito = True
                logger.info(f'Rio adicionado a favoritos: {rio.nome} por {request.user.email}')
            
            return Response({'favorito': favorito})
        except Exception as e:
            logger.error(f'Erro ao atualizar favorito: {str(e)}')
            return Response(
                {'detail': 'Erro ao atualizar favorito.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PontoRiscoListCreateView(generics.ListCreateAPIView):
    serializer_class = PontoRiscoSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsDefesaCivilAdminOrOwner]

    def get_queryset(self):
        rio_id = self.kwargs.get('rio_id')
        return PontoRisco.objects.filter(rio_id=rio_id).order_by('-criado_em')

    def perform_create(self, serializer):
        rio_id = self.kwargs.get('rio_id')
        rio = get_object_or_404(Rios, pk=rio_id)
        serializer.save(criado_por=self.request.user, rio=rio)
        logger.info(f'Novo ponto de risco criado: {rio.nome} por {self.request.user.email}')


class PontoRiscoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PontoRiscoSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsDefesaCivilAdminOrOwner]

    def get_queryset(self):
        return PontoRisco.objects.all()

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Ponto de risco atualizado: {serializer.instance.rio.nome}')

    def perform_destroy(self, instance):
        rio_nome = instance.rio.nome
        instance.delete()
        logger.info(f'Ponto de risco deletado: {rio_nome}')

