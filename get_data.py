from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.library.http import NBAStatsHTTP
import pandas as pd
import time
import requests

# Agregar un User-Agent para evitar bloqueos
NBAStatsHTTP._nba_headers['User-Agent'] = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
)

def get_players_list():
    nba_players = players.get_players()
    nba_players_df = pd.DataFrame(nba_players)
    nba_active_players = nba_players_df[nba_players_df['is_active'] == True]
    return nba_active_players['full_name'].tolist()

def get_teams_list():
    nba_teams = teams.get_teams()
    nba_teams_df = pd.DataFrame(nba_teams)
    return nba_teams_df['full_name'].tolist()

def get_player_id(player_full_name):
    player_info = players.find_players_by_full_name(player_full_name)
    return player_info[0].get('id')

def get_team_id(team_full_name):
    team_info = teams.find_teams_by_full_name(team_full_name)
    return team_info[0].get('id')

def get_shooting_chart_data(player_id, team_id, season_nullable, max_retries=5):
    """Obtiene datos de tiro con reintentos manuales"""
    for attempt in range(1, max_retries + 1):
        try:
            shot_chart = shotchartdetail.ShotChartDetail(
                team_id=team_id,
                player_id=player_id,
                season_nullable=season_nullable,
                context_measure_simple="FGA",
                timeout=60
            )
            return shot_chart.shot_chart_detail.get_data_frame()
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt} fallido: {e}")
            if attempt == max_retries:
                raise
            wait_time = attempt * 5  # Espera creciente: 5, 10, 15...
            print(f"Reintentando en {wait_time} segundos...")
            time.sleep(wait_time)
