import json

from dash import dash
import pandas as pd
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash

from util import create_network_graph
from visualization import plot


def init_dash(server, ):
    global dash_app
    dash_app = dash.Dash(server = server, routes_pathname_prefix = "/dashapp/")

    dash_app.layout = html.Div()


def update_dash(artist_data, related_artist_data):
    G = create_network_graph(artist_data, related_artist_data)
    fig = plot(G)
    dash_app.layout = html.Div(
        dcc.Graph(figure = fig)
    )
