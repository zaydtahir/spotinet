from util import *
import json
import plotly.offline as py
import plotly.graph_objects as go


def make_edge(x, y, width, color):
    return go.Scatter(x = x,
                      y = y,
                      line = dict(width = width,
                                  color = color),
                      hoverinfo = 'text',
                      text = "",
                      mode = 'lines')


def plot(network_graph):
    # GRAPH APPEARANCE SETTINGS
    node_size = 40
    edge_width = 5
    text_size = 10
    line_color = "darkslategrey"
    node_color = "#12813A"
    node_border_color = "darkslategrey"

    # Force Directed Layout
    pos = nx.fruchterman_reingold_layout(network_graph)

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
    node_trace = go.Scatter(x = [],
                            y = [],
                            text = [],
                            textposition = "top center",
                            textfont_size = text_size,
                            mode = 'markers+text',
                            hoverinfo = 'none',
                            marker = dict(color = [],
                                          opacity=1,
                                          size = [],
                                          line = dict(width=5,color=node_border_color)))


    for node in network_graph.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['marker']['color'] += tuple([node_color])
        node_trace['marker']['size'] += tuple(node_size for node in range(0, len(network_graph.nodes())))
        node_trace['text'] += tuple(['<b>' + node + '</b>'])

    # Customize layout
    layout = go.Layout(
        paper_bgcolor = 'rgba(0,0,0,0)',  # transparent background
        plot_bgcolor = 'rgba(0,0,0,0)',  # transparent 2nd background
        xaxis = {'showgrid': False, 'zeroline': False},  # no gridlines
        yaxis = {'showgrid': False, 'zeroline': False},  # no gridlines
    )
    # Create figure
    fig = go.Figure(layout = layout)
    # Add all edge traces
    for trace in edge_trace:
        fig.add_trace(trace)
    # Add node trace
    fig.add_trace(node_trace)
    # Remove legend
    fig.update_layout(showlegend = False)
    # Remove tick labels
    fig.update_xaxes(showticklabels = False)
    fig.update_yaxes(showticklabels = False)
    # Show figure
    fig.show()
    return fig


if __name__ == "__main__":
    with open('artist_data.json') as f:
        artist_data = json.load(f)
    with open('related_artist_data.json') as f:
        related_artist_data = json.load(f)

    G = create_network_graph(artist_data, related_artist_data)
    plot(G)
