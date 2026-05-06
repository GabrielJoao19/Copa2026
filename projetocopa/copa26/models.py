from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class ConfederacaoEnum(models.TextChoices):
    UEFA = 'uefa', 'UEFA'
    CONMEBOL = 'conmebol', 'Conmebol'
    CONCACAF = 'concacaf', 'Concacaf'
    AFC = 'afc', 'AFC'
    CAF = 'caf', 'CAF'
    OFC = 'ofc', 'OFC'

class PosicaoEnum(models.TextChoices):
    GOLEIRO = 'goleiro', 'Goleiro'
    ZAGUEIRO = 'zagueiro', 'Zagueiro'
    LATERAL = 'lateral', 'Lateral'
    VOLANTE = 'volante', 'Volante'
    MEIA = 'meia', 'Meia'
    ATACANTE = 'atacante', 'Atacante'

class FaseEnum(models.TextChoices):
    GRUPOS = 'grupos', 'Grupos'
    FASE32 = 'fase32', 'Fase32'
    OITAVAS = 'oitavas', 'Oitavas'
    QUARTAS = 'quartas', 'QUARTAS'
    SEMIFINAL = 'semifinal', 'Semifinal'
    FINAL = 'final', 'Final'

class StatusEnum(models.TextChoices):
    AGENDADO = 'agendado', 'Agendado'
    EM_ANDAMENTO = 'em_andamento', 'Em_andamento'
    ENCERRADO = 'encerrado', 'Encerrado'
    CANCELADO = 'cancelado', 'Cancelado'

class TipoEnum(models.TextChoices):
    GOL = 'gol', 'Gol'
    CARTAO_AMARELO = 'cartao_amarelo', 'Cartao_amarelo'
    CARTAO_VERMELHO = 'cartao_vermelho', 'Cartao_vermelho'
    GOL_CONTRA = 'gol_contra', 'Gol_contra'

class Grupo(models.Model):
    nome = models.CharField(max_length=1)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"Grupo: {self.nome}"


class Tecnico(models.Model):
    nome = models.CharField(max_length=150)
    nacionalidade = models.CharField(max_length=100)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome

class Selecao(models.Model):
    nome = models.CharField(max_length=100)#Nome completo da seleção
    sigla = models.CharField(max_length=3, unique=True)
    confederacao = models.CharField(choices=ConfederacaoEnum.choices)
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT,related_name='selecoes')
    tecnico = models.OneToOneField(Tecnico, on_delete=models.SET_NULL, null=True, related_name='selecao')
    escudo_url = models.URLField(blank=True)

    def __str__(self):
        return self.nome

class Jogador(models.Model):
    nome = models.CharField(max_length=150)
    nome_guerra = models.CharField(max_length=50)
    selecao = models.ForeignKey(Selecao, on_delete=models.PROTECT, related_name='jogadores')
    posicao = models.CharField(choices=PosicaoEnum.choices)
    numero_camisa = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(26)
        ]
    )
    data_nascimento = models.DateField()
    suspenso = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    

class Jogo(models.Model):
    selecao_mandante = models.ForeignKey(Selecao, on_delete=models.PROTECT, related_name='jogos_mandante')
    selecao_visitante = models.ForeignKey(Selecao, on_delete=models.PROTECT, related_name='jogos_visitante')
    fase = models.CharField(choices=FaseEnum.choices)
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT, null=True, blank=True)
    data_hora = models.DateTimeField()
    estadio = models.CharField(max_length=150, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    gols_mandante = models.PositiveSmallIntegerField(default=0)
    gols_visitante = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(choices=StatusEnum.choices)

    def __str__(self):
        return f'{self.selecao_mandante} X {self.selecao_visitante}'

class EventoJogo(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, related_name='eventos')
    jogador = models.ForeignKey(Jogador, on_delete=models.PROTECT, related_name='eventos')
    tipo = models.CharField(choices=TipoEnum.choices)
    minuto = models.PositiveSmallIntegerField()
    acrescimo = models.BooleanField(default=False)
    