from rest_framework import generics
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer

# Create your views here.

class UsuarioCreatedListView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer    
