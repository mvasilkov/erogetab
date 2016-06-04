from django.conf import settings
from django.core import serializers
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, **options):
        metafile_path = (settings.OUR_ROOT / 'metafile.json').as_posix()
        with open(metafile_path, 'r') as f:
            for game in serializers.deserialize('json', f):
                game.save()
