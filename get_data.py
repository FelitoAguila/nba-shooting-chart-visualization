from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.library.http import NBAStatsHTTP
import pandas as pd
import time
import requests
import warnings
import numpy as np
from urllib3.exceptions import InsecureRequestWarning
from cache_system import NBADataCache

# Suprimir warnings de SSL
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

# Inicializar sistema de caché
cache = NBADataCache(max_age_hours=48)  # Caché válido por 48 horas

# Configurar headers más robustos para evitar bloqueos (basado en main.py)
NBAStatsHTTP.headers = {
    'User-Agent': (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.nba.com',
    'Referer': 'https://www.nba.com/',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
}

# Configurar timeout más corto globalmente para fallar rápido
NBAStatsHTTP.timeout = 10  # Solo 10 segundos

def get_players_list():
    """Obtiene lista de jugadores con manejo de errores"""
    try:
        nba_players = players.get_players()
        nba_players_df = pd.DataFrame(nba_players)
        nba_active_players = nba_players_df[nba_players_df['is_active'] == True]
        return [{'label': name, 'value': name} for name in sorted(nba_active_players['full_name'].tolist())]
    except Exception as e:
        print(f"Error obteniendo jugadores: {e}")
        # Lista de respaldo con jugadores populares
        backup_players = [
            'LeBron James', 'Stephen Curry', 'Kevin Durant', 'Luka Dončić',
            'Giannis Antetokounmpo', 'Jayson Tatum', 'Nikola Jokic', 'Joel Embiid'
        ]
        return [{'label': name, 'value': name} for name in backup_players]

def get_teams_list():
    """Obtiene lista de equipos con manejo de errores"""
    try:
        nba_teams = teams.get_teams()
        nba_teams_df = pd.DataFrame(nba_teams)
        return [{'label': name, 'value': name} for name in sorted(nba_teams_df['full_name'].tolist())]
    except Exception as e:
        print(f"Error obteniendo equipos: {e}")
        # Lista de respaldo con todos los equipos
        backup_teams = [
            'Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets',
            'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets',
            'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers',
            'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat',
            'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
            'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns',
            'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors',
            'Utah Jazz', 'Washington Wizards'
        ]
        return [{'label': name, 'value': name} for name in backup_teams]

def get_player_id(player_full_name):
    """Obtiene ID del jugador con manejo de errores"""
    try:
        player_info = players.find_players_by_full_name(player_full_name)
        if player_info and len(player_info) > 0:
            return player_info[0].get('id')
        else:
            raise ValueError(f"Jugador '{player_full_name}' no encontrado")
    except Exception as e:
        print(f"Error obteniendo ID del jugador {player_full_name}: {e}")
        raise

def get_team_id(team_full_name):
    """Obtiene ID del equipo con manejo de errores"""
    try:
        team_info = teams.find_teams_by_full_name(team_full_name)
        if team_info and len(team_info) > 0:
            return team_info[0].get('id')
        else:
            raise ValueError(f"Equipo '{team_full_name}' no encontrado")
    except Exception as e:
        print(f"Error obteniendo ID del equipo {team_full_name}: {e}")
        raise

def get_shooting_chart_data(player_id, team_id, season_nullable, max_retries=1):
    """Obtiene datos de tiro con fallback inmediato a datos de ejemplo"""
    
    # Intentar obtener datos del caché primero
    print("🔍 Buscando datos en caché...")
    cached_data = cache.get_cached_data(player_id, team_id, season_nullable)
    
    if cached_data is not None:
        if cached_data:  # Si hay datos en caché
            df = pd.DataFrame(cached_data)
            print(f"✅ Datos del caché cargados: {len(df)} tiros")
            return df
        else:  # Si el caché indica que no hay datos
            print("ℹ️ Caché indica que no hay datos para esta consulta")
            return pd.DataFrame()
    
    # Intentar API una sola vez con timeout corto
    print("🌐 Intentando API de NBA (timeout corto)...")
    
    try:
        # Timeout muy corto para fallar rápido
        shot_chart = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            season_nullable=season_nullable,
            context_measure_simple='FGA',
            season_type_all_star='Regular Season',
            timeout=10,  # Solo 10 segundos
            headers=NBAStatsHTTP.headers
        )
        
        data_frames = shot_chart.get_data_frames()
        data = data_frames[0] if data_frames and len(data_frames) > 0 else pd.DataFrame()
        
        if data is not None and not data.empty:
            print(f"✅ Datos obtenidos de API: {len(data)} tiros encontrados")
            cache.save_to_cache(player_id, team_id, season_nullable, data)
            return data
        else:
            print("⚠️ API no devolvió datos, usando datos de ejemplo...")
            return generate_enhanced_sample_data(player_id, team_id, season_nullable)
            
    except Exception as e:
        print(f"❌ API falló rápidamente: {type(e).__name__}")
        print("🔄 Generando datos de ejemplo inmediatamente...")
        return generate_enhanced_sample_data(player_id, team_id, season_nullable)

def generate_enhanced_sample_data(player_id, team_id, season):
    """Genera datos de ejemplo mejorados cuando la API no está disponible (basado en main.py)"""
    print("🎯 Generando datos de ejemplo mejorados para demostración...")
    
    # Generar datos sintéticos realistas usando las técnicas de main.py
    np.random.seed(42)  # Para resultados consistentes
    
    # Zonas de tiro más realistas basadas en el conocimiento del main.py
    shot_zones = [
        # Pintura (alta concentración cerca del aro)
        {'x_range': (-80, 80), 'y_range': (-47, 100), 'count': 35, 'make_rate': 0.65, 'type': 'paint'},
        
        # Tiros libres (línea extendida)
        {'x_range': (-60, 60), 'y_range': (100, 190), 'count': 25, 'make_rate': 0.45, 'type': 'ft_extended'},
        
        # Medio rango (más realista)
        {'x_range': (-200, 200), 'y_range': (100, 230), 'count': 30, 'make_rate': 0.40, 'type': 'mid_range'},
        
        # Triples - esquinas izquierda (zona caliente)
        {'x_range': (-250, -200), 'y_range': (-47, 90), 'count': 15, 'make_rate': 0.38, 'type': 'left_corner_3'},
        
        # Triples - esquinas derecha (zona caliente)
        {'x_range': (200, 250), 'y_range': (-47, 90), 'count': 15, 'make_rate': 0.38, 'type': 'right_corner_3'},
        
        # Triples - arco superior (más intentos, menor porcentaje)
        {'x_range': (-180, 180), 'y_range': (200, 300), 'count': 25, 'make_rate': 0.35, 'type': 'above_break_3'},
        
        # Triples - ala izquierda
        {'x_range': (-220, -150), 'y_range': (150, 250), 'count': 12, 'make_rate': 0.33, 'type': 'left_wing_3'},
        
        # Triples - ala derecha  
        {'x_range': (150, 220), 'y_range': (150, 250), 'count': 12, 'make_rate': 0.33, 'type': 'right_wing_3'},
    ]
    
    shots = []
    
    for zone in shot_zones:
        for _ in range(zone['count']):
            # Generar coordenadas con distribución más realista
            x = np.random.normal(
                (zone['x_range'][0] + zone['x_range'][1]) / 2, 
                (zone['x_range'][1] - zone['x_range'][0]) / 6
            )
            y = np.random.normal(
                (zone['y_range'][0] + zone['y_range'][1]) / 2,
                (zone['y_range'][1] - zone['y_range'][0]) / 6
            )
            
            # Mantener dentro de los límites
            x = np.clip(x, zone['x_range'][0], zone['x_range'][1])
            y = np.clip(y, zone['y_range'][0], zone['y_range'][1])
            
            # Determinar si el tiro fue anotado basado en la zona
            made = 1 if np.random.random() < zone['make_rate'] else 0
            
            # Calcular distancia real del tiro (como en main.py)
            distance = np.sqrt(x**2 + y**2) / 10  # Convertir a pies
            
            # Determinar tipo de tiro basado en distancia
            if distance >= 22:  # Triple
                shot_type = '3PT Field Goal'
                shot_value = 3
                shot_zone_basic = 'Above the Break 3' if y > 100 else 'Corner 3'
            else:  # Doble
                shot_type = '2PT Field Goal'
                shot_value = 2
                if distance <= 8:
                    shot_zone_basic = 'Restricted Area'
                elif distance <= 16:
                    shot_zone_basic = 'In The Paint (Non-RA)'
                else:
                    shot_zone_basic = 'Mid-Range'
            
            # Crear entrada de tiro con todas las columnas necesarias
            shot_entry = {
                'LOC_X': x,
                'LOC_Y': y,
                'SHOT_MADE_FLAG': made,
                'SHOT_ATTEMPTED_FLAG': 1,
                'SHOT_TYPE': shot_type,
                'SHOT_ZONE_BASIC': shot_zone_basic,
                'SHOT_ZONE_AREA': zone['type'],
                'SHOT_DISTANCE': distance,
                'SHOT_VALUE': shot_value,
                'PLAYER_ID': player_id,
                'TEAM_ID': team_id,
                'SEASON': season,
                'GAME_ID': f"002{np.random.randint(10000, 99999)}",
                'GAME_DATE': f"{season[:4]}-{np.random.randint(10, 12):02d}-{np.random.randint(1, 28):02d}",
                'PERIOD': np.random.randint(1, 4),
                'MINUTES_REMAINING': np.random.randint(0, 12),
                'SECONDS_REMAINING': np.random.randint(0, 59),
                'EVENT_TYPE': 'Made Shot' if made else 'Missed Shot',
                'ACTION_TYPE': f"{shot_type} {['Jump Shot', 'Pullup Shot', 'Fadeaway'][np.random.randint(0, 3)]}"
            }
            
            shots.append(shot_entry)
    
    df = pd.DataFrame(shots)
    
    # Agregar estadísticas de resumen
    total_shots = len(df)
    made_shots = df['SHOT_MADE_FLAG'].sum()
    fg_percentage = (made_shots / total_shots * 100) if total_shots > 0 else 0
    
    threes_attempted = len(df[df['SHOT_VALUE'] == 3])
    threes_made = df[(df['SHOT_VALUE'] == 3) & (df['SHOT_MADE_FLAG'] == 1)].shape[0]
    three_pt_percentage = (threes_made / threes_attempted * 100) if threes_attempted > 0 else 0
    
    print(f"📊 Datos de ejemplo generados: {total_shots} tiros")
    print(f"   📈 FG%: {fg_percentage:.1f}% ({made_shots}/{total_shots})")
    print(f"   🎯 3P%: {three_pt_percentage:.1f}% ({threes_made}/{threes_attempted})")
    print(f"   ⚡ Nota: Estos son datos sintéticos para demostración")
    
    # Guardar datos de ejemplo en caché
    cache.save_to_cache(player_id, team_id, season, df)
    
    return df
