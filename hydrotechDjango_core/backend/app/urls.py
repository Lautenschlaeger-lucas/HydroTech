from django.contrib import admin
from django.urls import path
from usuarios.views import UsuarioCreatedListView, UsuarioRetriveUpdateDestroyView
from rios.views import RiosListCreateView, RiosRetrieveUpdateDestroyView


urlpatterns = [
    path('usuarios/', UsuarioCreatedListView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>', UsuarioRetriveUpdateDestroyView.as_view(), name='usuario-detail-view'),

    path('rios/', RiosListCreateView.as_view(), name='rios-list-create'),
    path('rios/<int:pk>', RiosRetrieveUpdateDestroyView.as_view(), name='rios-detail-view')


]
