from django.urls import path
from . import views

game = views.GameViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

artifact = views.ArtifactViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

data = views.DataViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

game_pk = views.GameViewSet.as_view({
    'delete': 'destroy'
})

artifact_pk = views.ArtifactViewSet.as_view({
    'put': 'update',
})

dashboard = views.DashboardViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    # Jogo
    path('api/game/', game, name='games'),

    # Artefato
    path('api/artifact/', artifact, name='artifacts'),
    path('api/artifact/<int:pk>', artifact_pk, name='artifacts'),
    path('api/artifact/game/<int:jogo>', views.getArtifactGame, name='artifactsgame'),

    # Data
    path('api/data/', data, name='data'),
    path('api/data/<int:jogo>', views.getDataGame, name='data'),

    # Identificador
    path('api/identifier/<int:jogo>', views.getIdentifierGame, name='idgame'),
    
    # Gerar dashboard
    path('gerar-dashboard/', views.gerarDashboard, name="gerardashboard"),
    path('gerar-dashboard-saved/', views.gerarDashboardSaved, name="gerardashboardsaved"),

    # Funções
    path('api/functions/', views.getFunctions, name='functions'),

    # Dashboard
    path('api/dashboard/', dashboard, name='dashboard'),
    path('api/dashboard/<int:jogo>', views.getDashboardGame, name='dashboardgame')
]