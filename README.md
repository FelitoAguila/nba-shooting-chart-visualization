# 🏀 NBA Shooting Chart Visualization

Una aplicación web interactiva para visualizar gráficos de tiros de jugadores de la NBA.

## 🚀 Características

- 📊 Gráficos de tiros interactivos con Plotly
- 🎯 Visualización de la cancha de basketball con dimensiones reales
- 🏀 Análisis por zonas (pintura, medio rango, triples)
- 💾 Sistema de caché inteligente
- 🔄 Datos de demostración automáticos cuando la API no está disponible
- 📱 Interfaz responsive con Bootstrap

## 🛠️ Instalación

### Prerrequisitos
- Python 3.10+
- pip

### Pasos de instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/rigo93acosta/nba-shooting-chart-visualization.git
cd nba-shooting-chart-visualization
```

2. **Crear entorno virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
# o
.venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## ▶️ Uso

### Ejecutar la aplicación
```bash
python app.py
```

### Acceder a la aplicación
Abrir el navegador en: `http://localhost:8050`

### Usar la interfaz
1. Seleccionar un **jugador** del dropdown
2. Seleccionar un **equipo** del dropdown  
3. Seleccionar una **temporada** del dropdown
4. Hacer clic en **"Generar Gráfico"**
5. Ver el shooting chart interactivo

## 📁 Estructura del proyecto

```
nba-shooting-chart-visualization/
├── app.py              # Archivo principal de la aplicación
├── layout.py           # Definición del layout de la interfaz
├── callbacks.py        # Lógica de callbacks de Dash
├── charts.py           # Funciones para generar gráficos
├── get_data.py         # Obtención y procesamiento de datos
├── cache_system.py     # Sistema de caché inteligente
├── requirements.txt    # Dependencias del proyecto
├── Procfile           # Para despliegue en Heroku/Render
├── LICENSE            # Licencia del proyecto
└── README.md          # Este archivo
```

## 🔧 Funcionalidades técnicas

### Sistema de Caché
- Caché automático de 48 horas para datos de la API
- Evita llamadas repetidas y mejora el rendimiento
- Almacenamiento en archivos JSON locales

### Datos de Demostración
- Cuando la API de NBA no está disponible, se generan datos sintéticos realistas
- 169 tiros distribuidos por zonas de la cancha
- Porcentajes de acierto realistas por zona

### Manejo de Errores
- Timeout optimizado (10 segundos máximo)
- Fallback automático a datos de ejemplo
- Interfaz siempre funcional

## 🌐 Despliegue

### Heroku
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Render
1. Conectar repositorio GitHub
2. Usar `python app.py` como comando de inicio
3. Desplegar automáticamente

## 📊 Datos

La aplicación utiliza:
- **NBA API** para datos reales de tiros
- **Datos sintéticos** como fallback
- **Sistema de caché** para optimizar rendimiento

## 🤝 Contribuir

1. Fork el repositorio
2. Crear una rama feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit los cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autores

**Felix Aguila** 
**Rigo Acosta** - [@rigo93acosta](https://github.com/rigo93acosta)

---

## 🔧 Solución de problemas

### La aplicación no carga datos
- ✅ **Normal**: La aplicación usa datos de demostración cuando la NBA API no está disponible
- ✅ **Funcional**: Los datos sintéticos permiten probar todas las funcionalidades

### Error de dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Puerto en uso
Cambiar el puerto en `app.py` línea 25:
```python
port = int(os.environ.get("PORT", 8051))  # Cambiar 8050 por 8051
```
