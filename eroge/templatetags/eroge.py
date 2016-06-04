from django import template

from eroge.utils import make_filename

register = template.Library()

@register.filter
def dlsite_picture(game):
    return '/pictures/dlsite/RJ%s.jpeg' % game.dlsite

@register.filter
def game_folder(game):
    return 'Eroge_dlsite'

@register.filter
def game_save_as(game):
    return '%s %s' % (str(game), make_filename(game))
