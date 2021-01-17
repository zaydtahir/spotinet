from util import *
import json
import plotly.offline as py
import plotly.graph_objects as go


def make_edge(x, y, width, color):
    return go.Scatter(x=x,
                      y=y,
                      line=dict(width=width,
                                color=color),
                      hoverinfo='text',
                      text="",
                      mode='lines')


def plot(network_graph, df):
    # GRAPH APPEARANCE SETTINGS
    # General
    edge_width = 1
    text_size = 10
    node_border_width = 1
    node_border_color = "#385a7c"
    line_color = "#385a7c"
    # Origin
    origin_node_size = 60
    origin_node_color = "#385a7c"
    # Genre
    genre_node_size = 20
    genre_node_color = "#2596be"
    # Artist
    artist_node_size = 10
    your_artist_node_color = "#f97171"
    rcmd_artist_node_color = "#b2eee6"

    # Force Directed Layout
    pos = nx.kamada_kawai_layout(network_graph)
    # pos = nx.spring_layout(network_graph, k=0.5)

    # create edge trace
    edge_trace = []
    for edge in network_graph.edges():
        artist_1 = edge[0]
        artist_2 = edge[1]

        x0, y0 = pos[artist_1]
        x1, y1 = pos[artist_2]

        trace = make_edge([x0, x1, None], [y0, y1, None], edge_width, line_color)
        edge_trace.append(trace)

    # Make a node trace
    node_trace = go.Scatter(x=[],
                            y=[],
                            text=[],
                            textposition="top center",
                            textfont_size=text_size,
                            mode='markers+text',
                            hoverinfo='text',
                            marker=dict(color=[],
                                        opacity=1,
                                        size=[],
                                        line=dict(width=node_border_width, color=node_border_color)))

    for node in network_graph.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

        # Origin
        if df[str(node)] == 0:
            node_trace['marker']['color'] += tuple([origin_node_color])
            node_trace['marker']['size'] += tuple([origin_node_size])

        # Genre
        elif df[str(node)] == 1:
            node_trace['marker']['color'] += tuple([genre_node_color])
            node_trace['marker']['size'] += tuple([genre_node_size])

        # Your Artists
        elif df[str(node)] == 2:
            node_trace['marker']['color'] += tuple([your_artist_node_color])
            node_trace['marker']['size'] += tuple([artist_node_size])

        # Recommended Artists
        elif df[str(node)] == 3:
            node_trace['marker']['color'] += tuple([rcmd_artist_node_color])
            node_trace['marker']['size'] += tuple([artist_node_size])

        node_trace['text'] += tuple(['<b>' + node + '</b>'])

    # Customize layout
    layout = go.Layout(
        paper_bgcolor='white',  # transparent background
        plot_bgcolor='white',  # transparent 2nd background
        xaxis={'showgrid': False, 'zeroline': False},  # no grid-lines
        yaxis={'showgrid': False, 'zeroline': False},  # no grid-lines
    )
    # Create figure
    fig = go.Figure(layout=layout)
    # Add all edge traces
    for trace in edge_trace:
        fig.add_trace(trace)
    # Add node trace
    fig.add_trace(node_trace)
    # Remove legend
    fig.update_layout(showlegend=False)
    # Remove tick labels
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    # Hover Update
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"))
    # Show figure
    # fig.show()
    return fig
