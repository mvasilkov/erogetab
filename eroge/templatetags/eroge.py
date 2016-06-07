from django import template

from eroge.utils import make_filename

register = template.Library()

@register.filter
def dlsite_picture(game):
    if game.dlsite:
        return '/pictures/dlsite/RJ%s.jpeg' % game.dlsite
    elif game.getchu:
        return '/pictures/getchu/%s.jpeg' % game.getchu

@register.filter
def game_folder(game):
    if game.dlsite:
        return 'Eroge_dlsite'
    elif game.getchu:
        return 'Eroge_getchu'

@register.filter
def game_save_as(game):
    return '%s %s' % (str(game), make_filename(game))
