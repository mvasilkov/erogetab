from django.shortcuts import render

from .models import Game

def index(request):
    games = Game.objects.order_by('-getchu', '-dlsite')

    return render(request, 'eroge/index.html', {'games': games})
