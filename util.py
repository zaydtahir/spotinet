import json

import pandas as pd
import requests
import networkx as nx
import matplotlib.pyplot as plt


def filter_artist_data(artist_data: dict, filter_dict: dict):
    """
    :param artist_data: Dict of top artists with all info
    :param filter_dict: Empty dict to fill
    :return: Dict of top artists with name and image
    """
    required_keys = [
        "name",
        "images"
    ]

    for artist in artist_data['items']:
        filter_dict[artist['id']] = {key: artist[key] for key in required_keys}

    return filter_dict


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
        related_artists_response = requests.get(related_artists_endpoint, headers = auth_header)
        related_artists_data = json.loads(related_artists_response.text)
        related_artists_list = []
        for related_artist in related_artists_data['artists']:
            related_artists_list.append(related_artist['id'])
        filter_dict[artist] = related_artists_list

    return filter_dict


def create_network_graph(artist_data, related_artist_data):
    """
    :param artist_data: Dict of top artists with name and image
    :param related_artist_data: Dict of artist Id's connected to list of related artists
    :return: networkX object
    """

    source = []
    target = []
    you = "You"

    # Add top artists and yourself to network graph
    for artist_ids in artist_data.keys():
        target.append(you)
        source.append(artist_data[artist_ids]["name"])

    for artist in related_artist_data.keys():
        for related_artist in related_artist_data[artist]:
            try:
                # Check if Related Artist is in top artists
                related_artist_name = artist_data[related_artist]["name"]

                source.append(artist_data[artist]["name"])
                target.append(related_artist_name)

            except KeyError:
                pass

    df = pd.DataFrame(list(zip(source, target)), columns = ["source", "target"])
    G = nx.from_pandas_edgelist(df, 'source', 'target')

    # Draws the Graph (testing purposes)
    # nx.draw(G, with_labels=True)
    # plt.show()

    return G
