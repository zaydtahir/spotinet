# Example Used: https://github.com/drshrey/spotify-flask-auth-example

import json

import dash as dash
from flask import Flask, request, redirect, render_template
import requests
from urllib.parse import quote
from dotenv import load_dotenv
import pandas as pd
import dash
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc

load_dotenv()
import os

from util import filter_artist_data, filter_related_artist_data

server = Flask(__name__)
dashapp = dash.Dash(__name__, server = server, url_base_pathname = '/dash/')

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x = "Fruit", y = "Amount", color = "City", barmode = "group")

dashapp.layout = html.Div(children = [
    html.H1(children = 'Hello Dash'),

    html.Div(children = '''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id = 'example-graph',
        figure = fig
    )
])

#  Client Keys
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://localhost"
PORT = 8080
REDIRECT_URI = "{}:{}/callback".format(CLIENT_SIDE_URL, PORT)
SCOPE = "user-top-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}


@server.route("/")
def index():
    return render_template("index.html")


@server.route("/login")
def login():
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@server.route("/callback")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data = code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    # refresh_token = response_data["refresh_token"]
    # token_type = response_data["token_type"]
    # expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # Get top Artists
    top_artists_endpoint = "{}/me/top/artists".format(SPOTIFY_API_URL)
    artists_response = requests.get(top_artists_endpoint, headers = authorization_header)
    artists_data = json.loads(artists_response.text)
    filtered_artists_data = {}
    filtered_artists_data = filter_artist_data(artists_data, filtered_artists_data)

    filtered_related_artists = {}
    filtered_related_artists = filter_related_artist_data(filtered_artists_data, filtered_related_artists, SPOTIFY_API_URL, authorization_header)

    display_arr = [filtered_related_artists]
    return render_template("displaytest.html", sorted_array = display_arr)


if __name__ == "__main__":
    server.run(debug = True, port = PORT)
