#JOGO SERA A CLASSE MAIS AJUSTADA
from rest_framework import serializers
from .models import *

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo

        fields = '__all__'

class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico

        fields = '__all__'

class SelecaoSerializer(serializers.ModelSerializer):
    tecnico_nome = serializers.CharField(
        source = 'tecnico.nome',
        read_only = True
    )

    class Meta:
        model = Selecao

        fields = ['id', 'nome', 'sigla', 'confederacao', 'grupo', 'escudo_url', 'tecnico_nome']

class JogadorSerializer(serializers.ModelSerializer):
    posicao_display = serializers.CharField(
        source = 'get_posicao_display',
        read_only = True
    )

    class Meta:
        model = Jogador

        fields = ['id', 'nome', 'nome_guerra', 'posicao_display', 'posicao', 'numero_camisa', 'data_nascimento', 'selecao']

class EventoJogoSerializer(serializers.ModelSerializer):

    jogador_nome = serializers.CharField(
        source = 'jogador.nome',
        read_only = True
    )

    tipo_display = serializers.CharField(
        source = 'get_tipo_display',
        read_only = True
    )

    class Meta:
        model = EventoJogo

        fields = ['id', 'jogador_nome', 'jogador', 'tipo_display', 'tipo', 'minuto', 'acrescimo']

class JogoSerializer(serializers.ModelSerializer):

    mandante_nome = serializers.CharField(
        source = 'selecao_mandante.nome',
        read_only = True
    )

    visitante_nome = serializers.CharField(
        source = 'selecao_visitante.nome',
        read_only = True
    )

    fase_display = serializers.CharField(
        source = 'get_fase_display',
        read_only = True
    )

    status_display = serializers.CharField(
        source = 'get_status_display',
        read_only = True
    )

    eventos = EventoJogoSerializer(many=True, read_only=True)

    resultado = serializers.SerializerMethodField()

    def get_resultado(self, obj):
        if obj.gols_mandante > obj.gols_visitante:
            return f"{obj.selecao_mandante.nome} venceu"
        elif obj.gols_mandante < obj.gols_visitante:
            return f"{obj.selecao_visitante.nome} venceu"
        else:
            return f"{obj.selecao_mandante.nome} x {obj.selecao_visitante.nome} empataram"

    def create(self, validated_data):
        eventos_data = validated_data.pop('eventos', [])
        
        jogo = Jogo.objects.create(**validated_data)

        for evento in eventos_data:
            EventoJogo.objects.create(jogo=jogo, **evento)

        return jogo

    class Meta:
        model = Jogo

        fields = ['id', 'mandante_nome', 'selecao_mandante', 'visitante_nome', 'selecao_visitante', 'fase_display', 'fase', 'grupo', 'data_hora', 'estadio', 'cidade', 'gols_mandante', 'gols_visitante', 'status_display', 'status', 'eventos', 'resultado']