from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import shotchartdetail
import pandas as pd

def get_players_list():
    """Function to return all NBA players full names"""
    nba_players = players.get_players()
    nba_players_df = pd.DataFrame(nba_players)
    nba_active_players = nba_players_df[nba_players_df['is_active']== True]
    players_list = nba_active_players['full_name'].tolist()
    return players_list

def get_teams_list():
    """Function to return all NBA teams full names"""
    nba_teams = teams.get_teams()
    nba_teams_df = pd.DataFrame(nba_teams)
    teams_list = nba_teams_df['full_name'].tolist()
    return teams_list

def get_player_id(player_full_name):
    player_info = players.find_players_by_full_name(player_full_name)
    return player_info[0].get('id')

def get_team_id (team_full_name):
    team_info = teams.find_teams_by_full_name(team_full_name)
    return team_info[0].get('id')

def get_shooting_chart_data(player_id, team_id, season_nullable):
    """Function to get shooting chart data"""
    shot_chart = shotchartdetail.ShotChartDetail(
        team_id=team_id,
        player_id=player_id,
        season_nullable=season_nullable,    # NBA season format: 'YYYY-YY'
    )
    return shot_chart.shot_chart_detail.get_data_frame()





