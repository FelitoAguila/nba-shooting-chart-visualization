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

# Configuración para Render
app.title = "🏀 NBA Shooting Chart"
server = app.server  # Importante para Render

app.layout = layout
register_callbacks(app)

if __name__ == "__main__":
    # Configuración para desarrollo local y producción
    port = int(os.environ.get("PORT", 8050))
    debug = os.environ.get("ENVIRONMENT") != "production"
    
    app.run_server(
        host="0.0.0.0",  # Importante para Render
        port=port,
        debug=debug
    )
