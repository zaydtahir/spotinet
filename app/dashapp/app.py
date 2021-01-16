from dash import dash
import pandas as pd
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash


def init_dash(server):
    dash_app = dash.Dash(server = server, routes_pathname_prefix = "/dashapp/")

    # The following is an example for testing, replace it with dash app code
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x = "Fruit", y = "Amount", color = "City", barmode = "group")

    dash_app.layout = html.Div(children = [
        html.H1(children = 'Hello Dash'),

        html.Div(children = '''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id = 'example-graph',
            figure = fig
        )
    ])
