from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Game(models.Model):
    sequence = models.SmallAutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f'Jogo: {self.nome}.'

class Artifact(models.Model):
    sequence = models.SmallAutoField(primary_key=True)
    id = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f'Artefato: {self.nome} ({self.id}).'

class Data(models.Model):
    sequence = models.BigAutoField(primary_key=True)
    id = models.TextField(null=True, blank=True)
    artifact = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    datahora = models.DateTimeField(default=timezone.localtime)

    def __str__(self):
        return f'Game: {str(self.game)}. ID: {str(self.id)}. Artifact: {str(self.artifact)}. Value: {self.value}.'

class Dashboard(models.Model):
    sequence = models.SmallAutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    info = models.TextField()

    def __str__(self) -> str:
        return f'Dashboard: {self.nome}.'