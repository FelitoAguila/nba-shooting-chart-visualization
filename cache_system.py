"""
Sistema de caché para datos de la NBA
"""
import json
import os
import time
from datetime import datetime, timedelta
import hashlib

class NBADataCache:
    def __init__(self, cache_dir="cache", max_age_hours=24):
        self.cache_dir = cache_dir
        self.max_age_hours = max_age_hours
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Crear directorio de caché si no existe"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _get_cache_key(self, player_id, team_id, season):
        """Generar clave única para el caché"""
        key_string = f"{player_id}_{team_id}_{season}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key):
        """Obtener ruta del archivo de caché"""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def _is_cache_valid(self, cache_path):
        """Verificar si el caché sigue siendo válido"""
        if not os.path.exists(cache_path):
            return False
        
        # Verificar edad del archivo
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        expiry_time = file_time + timedelta(hours=self.max_age_hours)
        
        return datetime.now() < expiry_time
    
    def get_cached_data(self, player_id, team_id, season):
        """Obtener datos del caché si están disponibles y válidos"""
        cache_key = self._get_cache_key(player_id, team_id, season)
        cache_path = self._get_cache_path(cache_key)
        
        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                print(f"📁 Datos obtenidos del caché (guardados: {data.get('timestamp', 'fecha desconocida')})")
                return data.get('shot_data', [])
            except Exception as e:
                print(f"⚠️ Error leyendo caché: {e}")
                return None
        
        return None
    
    def save_to_cache(self, player_id, team_id, season, shot_data):
        """Guardar datos en el caché"""
        cache_key = self._get_cache_key(player_id, team_id, season)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'player_id': player_id,
                'team_id': team_id,
                'season': season,
                'shot_data': shot_data.to_dict('records') if hasattr(shot_data, 'to_dict') else shot_data
            }
            
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            print(f"💾 Datos guardados en caché")
        except Exception as e:
            print(f"⚠️ Error guardando en caché: {e}")
    
    def clear_cache(self):
        """Limpiar todo el caché"""
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, filename))
            print("🗑️ Caché limpiado")
        except Exception as e:
            print(f"⚠️ Error limpiando caché: {e}")
