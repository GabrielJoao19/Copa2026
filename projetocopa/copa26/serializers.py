#JOGO SERA A CLASSE MAIS AJUSTADA
from rest_framework import serializers
from .models import *

class GrupoSerializer(serializers.Serializer):
    class Meta:
        model = Grupo

        fields = '__all__'

class TecnicoSerializer(serializers.Serializer):
    class Meta:
        model = Tecnico

        fields = '__all__'

class SelecaoSerializer(serializers.Serializer):
    class 
