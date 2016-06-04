from django.conf import settings
from django.core import serializers
from django.core.management.base import BaseCommand

from eroge.models import Game

class Command(BaseCommand):
    def handle(self, **options):
        metafile_path = (settings.OUR_ROOT / 'metafile.json').as_posix()
        json_serializer = serializers.get_serializer('json')()
        with open(metafile_path, 'w') as f:
            json_serializer.serialize(Game.objects.all(), stream=f)
