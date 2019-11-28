import requests
import json
from urllib.parse import urlencode


from .search_type import SearchType
from gal_stream.core import read_config


def _search(criteria, auth, search_type):

    conf = read_config()

    if not criteria:
        raise AttributeError('Parameter `criteria` is required.')

    q_type = search_type.name.lower()
    url_params = {
        'q': criteria,
        'type': q_type
    }
    enc_params = urlencode(url_params)
    url = f'{conf.base_url}/search?{enc_params}'

    headers = {'Authorization': f'Bearer {auth.access_token}'}
    response = requests.get(url, headers=headers)

    return json.loads(response.text)


def search_artist(criteria, auth):
    return _search(criteria, auth, SearchType.ARTIST)


def search_album(criteria, auth):
    return _search(criteria, auth, SearchType.ALBUM)


def search_playlist(criteria, auth):
    return _search(criteria, auth, SearchType.PLAYLIST)


def search_track(criteria, auth):
    return _search(criteria, auth, SearchType.TRACK)
