from django.shortcuts import render
from rios.models import Rios
from rios.serializers import RiosSerializer
from rest_framework import generics

# Create your views here.
class RiosListCreateView(generics.ListCreateAPIView):
    queryset = Rios.objects.all()
    serializer_class = RiosSerializer

class RiosRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rios.objects.all()
    serializer_class = RiosSerializer
    