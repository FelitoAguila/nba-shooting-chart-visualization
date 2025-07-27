# app.py

import dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks
import os

# Añadir FontAwesome para los iconos
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "🏀 NBA Shooting Chart"
app.layout = layout
register_callbacks(app)

# Required for Render: Expose the Flask server
server = app.server

if __name__ == "__main__":
    # Use environment variables for port and host
    port = int(os.environ.get("PORT", 8050))  # Default to 8050 for local development
    app.run(host="0.0.0.0", port=port, debug=False)
