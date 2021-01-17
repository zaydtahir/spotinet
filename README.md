# Spotify Artist Visualizer

# What it does
SpotiNet generates a network graph based on the user's Spotify library to display a dynamic and interactive interface to discover new music and view current trends. The user sits at the center of the diagram, with nodes branching out connecting their top genres, artists, and artist recommendations based on their top artists.

# How we built it
SpotiNet is built in Python, with a Flask application at its base, while incorporating HTML and CSS for front end purposes. Using NetworkX and Pandas, we created a network graph between the user, genres, and artists. A PlotLy Dash application was integrated with Flask to display SpotiNet’s interactive network graph.
