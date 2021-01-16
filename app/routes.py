import json
from urllib.parse import quote

import requests
from flask import current_app as app, redirect, request
from flask import render_template

from util import filter_artist_data, filter_related_artist_data, get_genre_list
from constants import *


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback")
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

    genre_list = []
    genre_list = get_genre_list(filtered_artists_data, genre_list)

    from .dashapp.app import update_dash

    # Open the testing files here and pass them in instead if wanted
    update_dash(filtered_artists_data, filtered_related_artists, genre_list)

    # return render_template("displaytest.html")
    return redirect("/dashapp/")
