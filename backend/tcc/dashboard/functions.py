from .models import Data, Artifact
from django.db.models import Sum, FloatField, Count, Avg
from django.db.models.functions import Cast
from abc import ABC, abstractmethod
import inspect

def get_functions():
    """
    Retorna as funções disponíveis
    """
    functions = []

    for chave, valor in globals().items():
        classe_concreta = valor

        if inspect.isclass(classe_concreta) and issubclass(classe_concreta, FunctionBase) and chave != 'FunctionBase':
            objeto_da_classe = classe_concreta()
            functions.append({
                'id': chave,
                'nome': objeto_da_classe.get_descricao()
            })

    return functions

def get_data(funcao: str, tipo: int, game: int, artefato: list, id: list, inicio: str, final: str) -> dict:
    """
    Chama a classe da função conforme o nome informado
    """

    if funcao in globals():
        classe_concreta = globals()[funcao]

        if issubclass(classe_concreta, FunctionBase):
            objeto_da_classe = classe_concreta()

            if len(id) == 0:
                id = [x['id'] for x in list(Data.objects.filter(game=game, id__isnull=False).values('id').distinct())]

            return objeto_da_classe.get_data(tipo, game, artefato, id, inicio, final)
        else:
            return {'error': f'A Classe {funcao} deve implementar FunctionBase.'}
    else:
        return {'error': f'Classe {funcao} não identificada.'}

class FunctionBase(ABC):
    """
    Classe abstrata para ser implementada ao criar uma função.
    """

    @abstractmethod
    def get_descricao(self):
        pass

    @abstractmethod
    def get_data(self, tipo: int, game: int, artefato: list, id: list, inicio: str, final: str):
        pass

class SumAll(FunctionBase):
    """
    Função que soma todos os valores de todos os artefatos e identificadores.
    """

    def get_descricao(self):
        return 'Somatório (Todos os artefatos)'

    def get_data(self, tipo: int, game: int, artefato: list, id: list, inicio: str, final: str):
        data = []

        for artef in artefato:
            art = Artifact.objects.get(id=artef, game_id=game)

            if art.type not in ['numeric', 'interval']:
                return {'error': 'Função não suportada para o artefato selecionado.'}

        if inicio and final:
            result = Data.objects.filter(
                game_id=game,
                artifact__in=artefato,
                id__in=id,
                datahora__range=(inicio, final)
                ).annotate(
                    float=Cast('value', FloatField())
                ).aggregate(
                    soma=Sum('float')
                )
        else:
            result = Data.objects.filter(
                game_id=game,
                artifact__in=artefato,
                id__in=id
                ).annotate(
                    float=Cast('value', FloatField())
                ).aggregate(
                    soma=Sum('float')
                )
        
        data.append(result['soma'])

        return {
            "type": tipo,
            "data": {
                "labels": ['Total'],
                "datasets": [
                    {
                        "label": "Valores", 
                        "data": data
                    },
                    ]
                }
            }

class SumId(FunctionBase):
    """
    Função que soma os valores agrupando por identificador e artefato
    """

    def get_descricao(self):
        return 'Somatório (Por identificador)'

    def get_data(self, tipo: int, game: int, artefato: list, id: list, inicio: str, final: str):
        
        labels = []
        datasets = []
        data = []

        for artef in artefato:
            art = Artifact.objects.get(id=artef, game_id=game)

            labels.append(art.nome)
        
        # Busca os registros que possuem identificador
        if inicio and final:
            identificador = list(Data.objects.filter(
                    game_id=game, 
                    id__in=id,
                    datahora__range=(inicio, final)
                ).values(
                    'id'
                ).distinct())
        else:
            identificador = list(Data.objects.filter(
                    game_id=game,
                    id__in=id
                ).values(
                    'id'
                ).distinct())

        # Cria um dataset por identificador somando os valores
        for identif in identificador:
            data = []
            for artef in artefato:
                if inicio and final:
                    result = Data.objects.filter(
                        game_id=game,
                        artifact=artef,
                        id=identif['id'],
                        datahora__range=(inicio, final)
                        ).annotate(
                            float=Cast('value', FloatField())
                        ).aggregate(
                            soma=Sum('float')
                        )
                else:
                    result = Data.objects.filter(
                        game_id=game,
                        artifact=artef,
                        id=identif['id']
                        ).annotate(
                            float=Cast('value', FloatField())
                        ).aggregate(
                            soma=Sum('float')
                        )

                if (result):
                    data.append(result['soma'])

            datasets.append({
                "label": identif['id'],
                "data": data
            })

        return {
            'type': tipo,
            'data': {
                'labels': labels,
                'datasets': datasets
            }
        }

class SumArtifact(FunctionBase):
    """
    Função que soma todos os valores agrupando por artefato
    """

    def get_descricao(self):
        return 'Somatório (Por artefato)'

    def get_data(self, tipo: int, game: int, artefato: list, id: list, inicio: str, final: str):
        data = []
        labels = []

        for artef in artefato:
            art = Artifact.objects.get(id=artef, game_id=game)

            if art.type not in ['numeric', 'interval']:
                return {'error': 'Função não suportada para o artefato selecionado.'}

            labels.append(art.nome)

            if inicio and final:
                result = Data.objects.filter(
                    game_id=game,
                    artifact=artef,
                    id__in=id,
                    datahora__range=(inicio, final)
                    ).annotate(
                        float=Cast('value', FloatField())
                    ).aggregate(
                        soma=Sum('float')
                    )
            else:
                result = Data.objects.filter(
                    game_id=game,
                    artifact=artef,
                    id__in=id
                    ).annotate(
                        float=Cast('value', FloatField())
                    ).aggregate(
                        soma=Sum('float')
                    )
            
            data.append(result['soma'])

        return {
            "type": tipo,
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Valores", 
                        "data": data
                    },
                    ]
                }
            }

class CountValue(FunctionBase):
    """
    Função que conta para cada valor a quantidade de vezes que possui o valor
    """

    def get_descricao(self):
        return 'Ocorrência (quantidade por valor)'

    def get_data(self, tipo: int, game: int, artefato: list, id: list, inicio: str, final: str):
        labels = []
        datasets = []
        valores = []

        # Busca a descrição dos artefatos
        for artef in artefato:
            art = Artifact.objects.get(id=artef, game_id=game)

            labels.append(art.nome)

        # Busca todos os valores distintos
        if inicio and final:
            valor_distinto = Data.objects.filter(
                    artifact__in=artefato,
                    id__in=id,
                    datahora__range=(inicio, final)
                ).values(
                    'value'
                ).annotate(
                    total=Count('value')
                )
        else:
            valor_distinto = Data.objects.filter(
                    artifact__in=artefato,
                    id__in=id
                ).values(
                    'value'
                ).annotate(
                    total=Count('value')
                )
        
        # Para cada valor busca a quantidade por artefato
        for item in valor_distinto:
            valores.append(item['value'])
            valor = item['value']
            dataart = []

            # Busca a quantidade de ocorrências do valor para cada artefato
            for artef in artefato:
                if inicio and final:
                    total = Data.objects.filter(
                            artifact=artef, 
                            value=valor,
                            id__in=id,
                            datahora__range=(inicio, final)
                        ).values(
                            'value'
                        ).aggregate(
                            total=Count('value')
                        )
                else:
                    total = Data.objects.filter(
                            artifact=artef, 
                            value=valor,
                            id__in=id
                        ).values(
                            'value'
                        ).aggregate(
                            total=Count('value')
                        )

                dataart.append(total['total'])
            
            datasets.append({
                "label": valor,
                "data": dataart 
            })

        return {
            "type": tipo,
            "data": {
                "labels": labels,
                "datasets": datasets
                }
            }

class CountArtifact(FunctionBase):
    """
    Função que conta a quantidade de vezes que o artefato possui valor
    """

    def get_descricao(self):
        return 'Ocorrência (quantidade por artefato)'

    def get_data(self, tipo: int, game: int, artefato: list, id: list, inicio: str, final: str):
        data = []
        labels = []

        for artef in artefato:
            art = Artifact.objects.get(id=artef, game_id=game)

            if art.type not in ['numeric', 'interval']:
                return {'error': 'Função não suportada para o artefato selecionado.'}

            labels.append(art.nome)

            if inicio and final:
                result = Data.objects.filter(
                        game_id=game,
                        artifact=artef,
                        id__in=id,
                        datahora__range=(inicio, final)
                    ).values(
                        'value'
                    ).aggregate(
                        total=Count('value')
                    )
            else:
                result = Data.objects.filter(
                        game_id=game,
                        artifact=artef,
                        id__in=id
                    ).values(
                        'value'
                    ).aggregate(
                        total=Count('value')
                    )

            data.append(result['total'])

        return {
            "type": tipo,
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Valores", 
                        "data": data
                    },
                    ]
                }
            }