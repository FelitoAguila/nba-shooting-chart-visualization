# app.py

import dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

# Añadir FontAwesome para los iconos
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "🏀 NBA Shooting Chart"
app.layout = layout
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)