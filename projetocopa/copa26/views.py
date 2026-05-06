from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

class TecnicoViewSet(viewsets.ModelViewSet):
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nome']

class SelecaoViewSet(viewsets.ModelViewSet):
    queryset = Selecao.objects.all()
    serializer_class = SelecaoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['grupo']
    search_fields = ['nome', 'sigla']

class JogadorViewSet(viewsets.ModelViewSet):
    queryset = Jogador.objects.select_related('selecao')
    serializer_class = JogadorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['selecao', 'posicao', 'suspenso']
    search_fields = ['nome', 'nome_guerra']
    ordering_fields = ['selecao', 'numero_camisa']

class EventoJogoViewSet(viewsets.ModelViewSet):
    queryset = EventoJogo.objects.select_related('jogador')
    serializer_class = EventoJogoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['jogador', 'tipo', 'jogo']

class JogoViewSet(viewsets.ModelViewSet):
    queryset = Jogo.objects.select_related('selecao_mandante', 'selecao_visitante').prefetch_related('eventos', 'eventos__jogador')
    serializer_class = JogoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['fase', 'status', 'grupo']
    search_fields = ['estadio', 'cidade']
    ordering_fields = ['data_hora']
