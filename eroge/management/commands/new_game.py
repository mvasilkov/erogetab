import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError

from eroge.models import Game
from eroge.utils import (HTTPError, get_game_id, get_html_page, get_picture,
                         cast_dlsite_j_to_e, normalize_eng_name)

BACKGROUND_IMAGE = re.compile(r'background-image: url\((.*?)\)')

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--dlsite', dest='dlsite')

    def handle(self, dlsite=None, **options):
        if dlsite is not None:
            self.game_dlsite(dlsite)
        else:
            raise CommandError('Bad game: no dlsite')

    def game_dlsite(self, dlsite):
        game_id = get_game_id(dlsite)
        assert game_id.startswith('RJ')
        existing = Game.objects.filter(dlsite=game_id[2:]).count()
        if existing != 0:
            raise CommandError('Duplicate game')

        html = get_html_page(dlsite)
        soup = BeautifulSoup(html, 'html5lib')

        name_a = soup.find(id='work_name').a
        name_a.span.decompose()
        name = next(name_a.stripped_strings)
        assert name

        visual_css = soup.find(id='work_visual').get('style')
        found = BACKGROUND_IMAGE.match(visual_css)
        assert found
        picture = urljoin(dlsite, found.group(1))
        get_picture(picture, 'dlsite', game_id=game_id)

        has_eng, name_eng = self.game_dlsite_eng(dlsite)

        game = Game(dlsite=game_id[2:], dlsite_name=name,
                    dlsite_has_eng=has_eng, dlsite_name_eng=name_eng)
        self.stdout.write(self.style.SUCCESS('Saving to database: %s' % game))
        game.save()

    def game_dlsite_eng(self, dlsite):
        dlsite_eng = cast_dlsite_j_to_e(dlsite)

        try:
            html = get_html_page(dlsite_eng)
        except HTTPError as err:
            if err.status_code == 404:
                return False, ''
            raise

        soup = BeautifulSoup(html, 'html5lib')

        name_a = soup.find(id='work_name').a
        name_a.span.decompose()
        name = next(name_a.stripped_strings)
        assert name

        return True, normalize_eng_name(name)
