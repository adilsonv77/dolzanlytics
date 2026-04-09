from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from .models import Game, Artifact, Data, Dashboard
from .serializers import DashboardSerializer, GameSerializer, ArtifactSerializer, DataSerializer
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse, HttpRequest
import json
from . import functions

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class ArtifactViewSet(viewsets.ModelViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    
    def create(self, request):
        data = request.data

        artifact = data.get('artifact')

        if not Artifact.objects.filter(id=artifact).first():
           return HttpResponseNotFound('Artefato não encontrado')

        return super().create(request)

class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer

@api_view(['GET'])
def getIdentifierGame(request, jogo):
    """
    Busca os identificadores que o jogo possui
    """
    data = list(Data.objects.filter(game=jogo, id__isnull=False).values('id').distinct())

    return JsonResponse(data, safe=False)
    
@api_view(['GET'])
def getArtifactGame(request, jogo):
    """
    Busca os artefatos do jogo
    """
    data = list(Artifact.objects.filter(game=jogo).values()) 

    return JsonResponse(data, safe=False)

@api_view(['GET'])
def getDataGame(request, jogo):
    """
    Retorna os dados do jogo
    """
    data = list(Data.objects.filter(game=jogo).values()) 

    return JsonResponse(data, safe=False)

@api_view(['POST'])
def gerarDashboard(request: HttpRequest):
    """
    Gera o dashboard e retorna as informações
    """
    res = request.body
    json_str = res.decode('utf-8')
    json_dict = json.loads(json_str)

    game = json_dict["game"]
    id = json_dict["id"]
    artefato = json_dict["artefato"]
    funcao = json_dict["funcao"]
    tipo = json_dict['tipo']
    inicio = json_dict['inicio']
    final = json_dict['final']

    resposta = functions.get_data(funcao, tipo, game, artefato, id, inicio, final)
    
    return JsonResponse(resposta)

@api_view(['POST'])
def gerarDashboardSaved(request: HttpRequest):
    """
    Gera o dashboard conforme salvo
    """
    res = request.body
    json_str = res.decode('utf-8')
    json_dict = json.loads(json_str)

    sequence = json_dict["sequence"]

    dashboard = Dashboard.objects.filter(sequence=sequence).first()
    
    json_dict = json.loads(dashboard.info)

    game = dashboard.game
    id = json_dict["id"]
    artefato = json_dict["artefato"]
    funcao = json_dict["funcao"]
    tipo = json_dict['tipo']
    inicio = json_dict['inicio']
    final = json_dict['final']

    resposta = functions.get_data(funcao, tipo, game, artefato, id, inicio, final)
    
    return JsonResponse(resposta)

@api_view(['GET'])
def getFunctions(request: HttpRequest):
    """
    Retorna as funções disponíveis
    """

    return JsonResponse(functions.get_functions(), safe=False)

@api_view(['GET'])
def getDashboardGame(request, jogo):
    """
    Retorna os dashboards salvos do jogo
    """
    data = list(Dashboard.objects.filter(game=jogo).values()) 

    return JsonResponse(data, safe=False)