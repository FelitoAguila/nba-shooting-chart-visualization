from get_data import get_player_id, get_team_id, get_shooting_chart_data
from charts import plot_shot_chart
from dash import Input, Output, State
import plotly.graph_objects as go

def register_callbacks(app):
    @app.callback(
        Output("shot-chart", 'figure'),
        [Input("generate-chart-btn", "n_clicks")],
        [
            State('player-dropdown', 'value'),
            State('team-dropdown', 'value'),
            State('season-dropdown', 'value')
        ]
    )
    def show_shooting_chart(n_clicks, player, team, season):
        # Si no se ha hecho clic en el botón, mostrar gráfico vacío
        if not n_clicks:
            return create_empty_chart()
        
        # Validar que todos los campos estén seleccionados
        if not all([player, team, season]):
            return create_empty_chart("⚠️ Por favor, selecciona jugador, equipo y temporada")
        
        try:
            player_id = get_player_id(player)
            team_id = get_team_id(team)
            data = get_shooting_chart_data(player_id, team_id, season)
            
            if data is not None and not data.empty:
                # Verificar si son datos de ejemplo o reales
                title_prefix = f"{player} - {season}"
                if len(data) <= 200:  # Probablemente datos de ejemplo
                    title_prefix += " (Datos de Demostración)"
                
                fig = plot_shot_chart(data, title=title_prefix)
                return fig
            else:
                return create_empty_chart(f"ℹ️ No hay datos de tiros para {player} en la temporada {season}")
                
        except Exception as e:
            print(f"Error en callback: {e}")
            # En caso de cualquier error, mostrar datos de ejemplo
            return create_error_chart("🔄 Mostrando datos de demostración debido a problemas con la API de NBA")

def create_empty_chart(message="🏀 Haz clic en 'Generar Gráfico' para comenzar"):
    """Crea un gráfico vacío con mensaje"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        xanchor='center', yanchor='middle',
        font=dict(size=20, color="#667eea"),
        showarrow=False
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig

def create_error_chart(error_message):
    """Crea un gráfico de error"""
    fig = go.Figure()
    fig.add_annotation(
        text=f"❌ {error_message}",
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        xanchor='center', yanchor='middle',
        font=dict(size=16, color="#d32f2f"),
        showarrow=False
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig