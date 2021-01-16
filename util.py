import json

import requests


def filter_artist_data(artist_data: dict, filter_dict: dict):
    required_keys = [
        "name",
        "images"
    ]

    for artist in artist_data['items']:
        filter_dict[artist['id']] = {key: artist[key] for key in required_keys}

    return filter_dict


def filter_related_artist_data(artist_data: dict, filter_dict: dict, spotify_api_url, auth_header):
    required_keys = [
        "name",
    ]

    for artist in artist_data:
        related_artists_endpoint = "{}/artists/{}/related-artists".format(spotify_api_url, artist)
        related_artists_response = requests.get(related_artists_endpoint, headers = auth_header)
        related_artists_data = json.loads(related_artists_response.text)
        related_artists_dict = {}
        for related_artist in related_artists_data['artists']:
            related_artists_dict[related_artist['id']] = {key: related_artist[key] for key in required_keys}
        filter_dict[artist] = related_artists_dict

    return filter_dict
