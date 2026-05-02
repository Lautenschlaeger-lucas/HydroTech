from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Rios, PontoRisco
from .serializers import RiosSerializer, PontoRiscoSerializer
from usuarios.authentication import JWTOrAPITokenAuthentication
from usuarios.permissions import IsDefesaCivilAdminOrOwner


class RiosListCreateView(generics.ListCreateAPIView):
    serializer_class = RiosSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rios.objects.filter(criado_por=self.request.user)

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class RiosRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiosSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rios.objects.filter(criado_por=self.request.user)


class RiosFavoriteView(APIView):
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        rio = get_object_or_404(Rios, pk=pk, criado_por=request.user)
        if request.user.favoritos.filter(pk=rio.pk).exists():
            request.user.favoritos.remove(rio)
            favorito = False
        else:
            request.user.favoritos.add(rio)
            favorito = True
        return Response({'favorito': favorito})


class PontoRiscoListCreateView(generics.ListCreateAPIView):
    serializer_class = PontoRiscoSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsDefesaCivilAdminOrOwner]

    def get_queryset(self):
        rio_id = self.kwargs.get('rio_id')
        return PontoRisco.objects.filter(rio_id=rio_id)

    def perform_create(self, serializer):
        rio_id = self.kwargs.get('rio_id')
        rio = get_object_or_404(Rios, pk=rio_id)
        serializer.save(criado_por=self.request.user, rio=rio)


class PontoRiscoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PontoRiscoSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsDefesaCivilAdminOrOwner]

    def get_queryset(self):
        return PontoRisco.objects.all()
