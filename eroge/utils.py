from os import path
import re
import shutil
from urllib.parse import urlparse

import requests

DLSITE_J = re.compile(r'^http://www\.dlsite\.com/maniax/work/=/product_id/(RJ\d{6})\.html$')
DLSITE_E = re.compile(r'^http://www\.dlsite\.com/ecchi-eng/work/=/product_id/(RE\d{6})\.html$')

MAKE_DLSITE_J = 'http://www.dlsite.com/maniax/work/=/product_id/%s.html'
MAKE_DLSITE_E = 'http://www.dlsite.com/ecchi-eng/work/=/product_id/%s.html'

def _override_filename(name):
    from .models import OverrideFilename

    if not _override_filename.cache:
        _override_filename.cache = dict(OverrideFilename.objects.values_list('name', 'filename'))

    return _override_filename.cache.get(name, None)

_override_filename.cache = None

class HTTPError(RuntimeError):
    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        return 'HTTP Error: ' + self.status_code

def get_game_id(address):
    for regex in DLSITE_J, DLSITE_E:
        found = regex.match(address)
        if found:
            return found.group(1)

    raise ValueError('Bad address: ' + address)

def get_cache_path(address):
    found = DLSITE_J.match(address)
    if found:
        return 'cache/dlsite/%s.html' % found.group(1)

    found = DLSITE_E.match(address)
    if found:
        return 'cache/dlsite_eng/%s.html' % found.group(1)

    raise ValueError('Bad address: ' + address)

def get_html_page(address):
    cache_path = get_cache_path(address)

    if path.isfile(cache_path):
        print('Found page in cache: ' + cache_path)
        return open(cache_path, encoding='utf8').read()

    print('Loading page: ' + address)
    r = requests.get(address)
    if r.status_code != 200:
        raise HTTPError(r.status_code)

    with open(cache_path, 'w', encoding='utf8') as f:
        f.write(r.text)

    return r.text

def get_picture(address, subpath, game_id=None, game_address=None):
    assert game_id is not None or game_address is not None
    if game_id is None:
        game_id = get_game_id(game_address)

    address_path = urlparse(address).path
    extension = path.splitext(address_path)[1]
    if extension == '.jpg':
        extension = '.jpeg'
    assert extension in ('.jpeg', '.png')
    picture_path = 'pictures/%s/%s%s' % (subpath, game_id, extension)

    if path.isfile(picture_path):
        print('Found picture in cache: ' + picture_path)
        return picture_path

    print('Loading picture: ' + address)
    r = requests.get(address, stream=True)
    if r.status_code != 200:
        raise HTTPError(r.status_code)

    with open(picture_path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    return picture_path

def cast_dlsite_j_to_e(address):
    game_id = get_game_id(address).replace('RJ', 'RE')
    return MAKE_DLSITE_E % game_id

def normalize_eng_name(name):
    name = name.replace('AssGape(r)', 'AssGape®')
    return name

def make_filename(game):
    if game.dlsite_has_eng:
        name = game.dlsite_name_eng
        # Game-specific cleanup
        result = _override_filename(name)
        if result:
            return result
        # Common cleanup
        name = re.sub(r' -.*?-$', '', name)
        name = re.sub(r' ~.*?~$', '', name)
        name = name.replace('*', '■')
        name = re.sub(r'[^\w ■]', '', name)
    else:
        name = game.dlsite_name
        # Fullwidth chars
        name = name.replace('?', '？')
        name = name.replace('!', '！')
        name = name.replace(':', '：')
        name = name.replace('*', '＊')

    return name
