# layout.py

import dash_bootstrap_components as dbc
from dash import dcc, html
from get_data import get_players_list, get_teams_list

layout = dbc.Container([
    # Header mejorado con gradiente y sombra
    html.Div([
        html.H1("🏀 NBA Shooting Chart", 
                className="text-center mb-0",
                style={
                    'color': '#ffffff',
                    'fontWeight': 'bold',
                    'fontSize': '3rem',
                    'textShadow': '2px 2px 4px rgba(0,0,0,0.3)'
                }),
        html.P("Analiza los tiros de tus jugadores favoritos",
               className="text-center text-light mb-0",
               style={'fontSize': '1.2rem', 'opacity': '0.9'})
    ], 
    className="py-5 mb-4",
    style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'borderRadius': '15px',
        'boxShadow': '0 10px 30px rgba(0,0,0,0.2)'
    }),

    # Panel de controles con tarjeta elegante
    dbc.Card([
        dbc.CardBody([
            html.H4("🎯 Configuración", 
                   className="text-center mb-4",
                   style={'color': '#333', 'fontWeight': 'bold'}),
            
            dbc.Row([
                dbc.Col([
                    html.Label("👤 Jugador", 
                             className="mb-2",
                             style={'fontWeight': 'bold', 'color': '#555'}),
                    dcc.Dropdown(
                        id='player-dropdown',
                        options=get_players_list(),  
                        value='Luka Dončić',
                        placeholder="Selecciona un jugador",
                        className="mb-3",
                        style={
                            'borderRadius': '10px',
                            'border': '2px solid #e3f2fd'
                        }
                    ),
                ], md=4),

                dbc.Col([
                    html.Label("🏆 Equipo", 
                             className="mb-2",
                             style={'fontWeight': 'bold', 'color': '#555'}),
                    dcc.Dropdown(
                        id='team-dropdown',
                        options=get_teams_list(),  
                        value='Dallas Mavericks',
                        placeholder="Selecciona un equipo",
                        className="mb-3",
                        style={
                            'borderRadius': '10px',
                            'border': '2px solid #e8f5e8'
                        }
                    ),
                ], md=4),

                dbc.Col([
                    html.Label("📅 Temporada", 
                             className="mb-2",
                             style={'fontWeight': 'bold', 'color': '#555'}),
                    dcc.Dropdown(
                        id='season-dropdown',
                        options=['2024-25', '2023-24'],
                        value='2024-25',
                        placeholder="Selecciona una temporada",
                        className="mb-3",
                        style={
                            'borderRadius': '10px',
                            'border': '2px solid #fff3e0'
                        }
                    ),
                ], md=4),
            ]),

            # Botón centrado con diseño atractivo
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        [
                            html.I(className="fas fa-chart-line me-2"),
                            "Generar Gráfico"
                        ],
                        id="generate-chart-btn",
                        color="primary",
                        size="lg",
                        className="mt-3",
                        style={
                            'background': 'linear-gradient(45deg, #667eea, #764ba2)',
                            'border': 'none',
                            'borderRadius': '25px',
                            'padding': '12px 30px',
                            'fontWeight': 'bold',
                            'fontSize': '1.1rem',
                            'boxShadow': '0 4px 15px rgba(102, 126, 234, 0.4)',
                            'transition': 'all 0.3s ease',
                            'transform': 'translateY(0px)'
                        }
                    )
                ], className="text-center")
            ])
        ])
    ], 
    className="mb-4",
    style={
        'borderRadius': '15px',
        'boxShadow': '0 5px 20px rgba(0,0,0,0.1)',
        'border': 'none'
    }),

    # Contenedor del gráfico con diseño mejorado
    dbc.Card([
        dbc.CardBody([
            html.H4("📊 Gráfico de Tiros", 
                   className="text-center mb-4",
                   style={'color': '#333', 'fontWeight': 'bold'}),
            
            dcc.Loading(
                id="loading-graph",
                type="cube",
                color="#667eea",
                style={'height': '60px'},
                children=[
                    dcc.Graph(
                        id="shot-chart",
                        style={
                            'height': '600px',
                            'borderRadius': '10px'
                        }
                    )
                ]
            )
        ])
    ],
    className="mx-auto",
    style={
        'borderRadius': '15px',
        'boxShadow': '0 5px 20px rgba(0,0,0,0.1)',
        'border': 'none',
        'minHeight': '650px',
        'maxWidth': '650px'
    }),

], fluid=True, style={'backgroundColor': '#f5f7fa', 'minHeight': '100vh', 'padding': '20px'})

