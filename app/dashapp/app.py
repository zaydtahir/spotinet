import json

from dash import dash
import pandas as pd
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash
from dash.dependencies import Input, Output

from app.routes import get_auth_header
from constants import SPOTIFY_API_URL
from util import *
from visualization import *
from constants import *

def init_dash(server):
    global dash_app
    dash_app = dash.Dash(server = server, routes_pathname_prefix = "/dashapp/")

    dash_app.layout = html.Div()

    init_callbacks(dash_app)

    return dash_app.server


def update_dash(artist_data, related_artist_data, genre_list):
    df = build_dict(artist_data, related_artist_data, genre_list)
    G = create_network_graph(artist_data, related_artist_data, genre_list)
    fig = plot(G, df)
    dash_app.layout = html.Div([
        dcc.Graph(id = 'graph', figure = fig, style = {'height': '100vh', 'width': '90%', 'left': '0', 'margin-left': '0px', 'display': 'inline-block'}),
        html.Div([
            html.A(html.Button(id = 'artist-name', style = {'display': 'none'}), id = 'artist-link', target = '_blank'),
            html.Img(id = 'artist-image', style = {'width': '95%'})
        ], style = {'display': 'inline-block', 'top': '300px', 'position': 'fixed'}),
    ],
        style = {'height': '100vh'}
    )


def init_callbacks(dash_app):
    @dash_app.callback(
        Output('artist-name', 'children'),
        Output('artist-name', 'style'),
        Output('artist-image', 'src'),
        Output('artist-link', 'href'),
        Input('graph', 'clickData'))
    def display_click_data(clickData):
        if clickData['points'][0]['marker.color'] not in ['#b2eee6','#f97171']:
            return
        else:

            artist_name = clickData['points'][0]['text'][3:-4]
            artist_endpoint = "{}/search?query={}&type=artist&offset=0&limit=1".format(SPOTIFY_API_URL, artist_name.replace(' ', '%20'))
            artist_response = requests.get(artist_endpoint, headers = get_auth_header())
            artist_data = json.loads(artist_response.text)
            artist_data = artist_data['artists']['items'][0]

            return artist_name, {
                'width': '95%', 'background-color': '#f97171', 'border': 'none', 'color': 'white',
                'padding': '30 px 32 px', 'text-align': 'center', 'text-decoration': 'none', 'font-size': '16px'
            },  artist_data['images'][0]['url'], artist_data['external_urls']['spotify']
