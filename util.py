import json

import pandas as pd
import requests
import networkx as nx


def filter_artist_data(artist_data: dict, filter_dict: dict):
    """
    :param artist_data: Dict of top artists with all info
    :param filter_dict: Empty dict to fill
    :return: Dict of top artists with name and image
    """
    required_keys = [
        "name",
        "images",
        "genres"
    ]

    for artist in artist_data['items']:
        filter_dict[artist['id']] = {key: artist[key] for key in required_keys}

    return filter_dict


def get_genre_list(filtered_artist_data: dict, genre_list: list):
    for artist in filtered_artist_data:
        for genre in filtered_artist_data[artist]['genres']:
            if genre not in genre_list:
                genre_list.append(genre)
    return genre_list


def filter_related_artist_data(artist_data: dict, filter_dict: dict, spotify_api_url, auth_header):
    """
    :param artist_data: Dict of top artists with name and images
    :param filter_dict: Empty dict to fill
    :param spotify_api_url: Spotify API Base URL
    :param auth_header: Authentication Header for User
    :return: Dict of top Artist ID's to list of related artist ID's
    """
    required_keys = [
        "name",
    ]

    for artist in artist_data:
        related_artists_endpoint = "{}/artists/{}/related-artists".format(spotify_api_url, artist)
        related_artists_response = requests.get(related_artists_endpoint, headers=auth_header)
        related_artists_data = json.loads(related_artists_response.text)
        related_artists_dict = {}
        for related_artist in related_artists_data['artists']:
            related_artists_dict[related_artist['id']] = related_artist['name']
        filter_dict[artist] = related_artists_dict

    return filter_dict


def build_df(artist_data, related_artist_data, genre_list):
    """
    :param artist_data: Dict of top artists with name and image
    :param related_artist_data: Dict of artist Id's connected to list of related artists
    :param genre_list: List of Genres User listens to
    :return: Pandas Data Frame with node types mapped to node names
    """
    # node types: 0 = origin, 1 = genre, 2 = artist, 3 = related artist
    name = ["You"]
    node_type = [0]

    for genre in genre_list:
        name.append(genre)
        node_type.append(1)

    for artist in artist_data.keys():
        name.append(artist_data[artist]["name"])
        node_type.append(2)

    for artist in related_artist_data.keys():
        try:
            x = artist_data[artist]["name"]
        except KeyError:
            name.append(related_artist_data[artist]["name"])
            node_type.append(3)

    df = pd.DataFrame(list(zip(name, node_type)), columns=['name', 'node_type'])

    return df


def create_network_graph(artist_data, related_artist_data, genre_list):
    """
    :param artist_data: Dict of top artists with name and image
    :param related_artist_data: Dict of artist Id's connected to list of related artists
    :param genre_list: List of Genres User listens to
    :return: networkX object
    """

    source = []
    target = []

    you = "You"

    # Add genres and yourself to network graph
    for genre in genre_list:
        target.append(you)
        source.append(genre)

    # Connect artist to genres
    for artist in artist_data.keys():
        for genre in artist_data[artist]['genres']:
            source.append(genre)
            target.append(artist_data[artist]['name'])

    # Connect artists together
    for related_artist in related_artist_data.keys():
        for artist in related_artist_data[related_artist].keys():
            source.append(related_artist_data[related_artist][artist])
            target.append(artist_data[related_artist]['name'])

    df = pd.DataFrame(list(zip(source, target)), columns=["source", "target"])
    G = nx.from_pandas_edgelist(df, 'source', 'target')

    # Draws the Graph (testing purposes)
    # nx.draw(G, with_labels=True)
    # plt.show()

    return G
