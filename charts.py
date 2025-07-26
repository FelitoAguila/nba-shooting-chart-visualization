import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import plotly.graph_objects as go
import math
import numpy as np

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If no axis is provided, get current one
    if ax is None:
        ax = plt.gca()

    # Create the basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Free throw arcs
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')

    # Restricted area
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three point line
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center court
    center_outer = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw,
                     restricted, corner_three_a, corner_three_b, three_arc, center_outer, center_inner]

    if outer_lines:
        # Draw the outer lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)

    return ax

def create_arc_path(radius, center, start_angle, end_angle):
    """Crea un path SVG para un arco."""
    cx, cy = center
    
    # Convertir ángulos a radianes
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    
    # Calcular puntos inicial y final
    x1 = cx + radius * math.cos(start_rad)
    y1 = cy + radius * math.sin(start_rad)
    x2 = cx + radius * math.cos(end_rad)
    y2 = cy + radius * math.sin(end_rad)
    
    # Determinar si el arco es mayor a 180 grados
    large_arc = 1 if abs(end_angle - start_angle) > 180 else 0
    
    return f"M {x1},{y1} A {radius},{radius} 0 {large_arc},1 {x2},{y2}"

def create_semicircle_path(radius, center, top_half=True):
    """Crea un path SVG para una semicircunferencia completa."""
    cx, cy = center
    
    if top_half:
        # Semicircunferencia superior (de izquierda a derecha)
        x1, y1 = cx - radius, cy
        x2, y2 = cx + radius, cy
        sweep_flag = 0  # Dirección antihoraria para semicírculo superior
    else:
        # Semicircunferencia inferior (de izquierda a derecha)
        x1, y1 = cx - radius, cy
        x2, y2 = cx + radius, cy
        sweep_flag = 1  # Dirección horaria para semicírculo inferior
    
    return f"M {x1} {y1} A {radius} {radius} 0 0 {sweep_flag} {x2} {y2}"

def add_court_shapes(fig):
    """Añade todas las líneas de la cancha de basketball como shapes de Plotly."""
    shapes = []
    
    # Configuración de colores y estilos
    court_color = '#2C3E50'  # Azul oscuro elegante
    line_width = 3
    
    # === ARO Y TABLERO ===
    # Aro (círculo)
    shapes.append(dict(
        type='circle',
        xref='x', yref='y',
        x0=-7.5, y0=-7.5, x1=7.5, y1=7.5,
        line=dict(color='#E74C3C', width=line_width + 1)  # Rojo para el aro
    ))
    
    # Tablero
    shapes.append(dict(
        type='rect',
        x0=-30, y0=-7.5, x1=30, y1=-8.5,
        line=dict(color=court_color, width=line_width),
        fillcolor='rgba(44, 62, 80, 0.1)'
    ))
    
    # === ÁREA DE PINTURA ===
    # Caja exterior (paint)
    shapes.append(dict(
        type='rect',
        x0=-80, y0=-47.5, x1=80, y1=142.5,
        line=dict(color=court_color, width=line_width),
        fillcolor='rgba(52, 152, 219, 0.05)'
    ))
    
    # Caja interior
    shapes.append(dict(
        type='rect',
        x0=-60, y0=-47.5, x1=60, y1=142.5,
        line=dict(color=court_color, width=line_width)
    ))
    
    # === TIROS LIBRES ===
    # Generar puntos para semicircunferencia superior de tiros libres
    ft_radius = 60
    ft_center = (0, 142.5)
    
    # Semicircunferencia superior (línea sólida)
    ft_upper_points_x = []
    ft_upper_points_y = []
    for angle in np.linspace(0, np.pi, 30):
        x = ft_center[0] + ft_radius * np.cos(angle)
        y = ft_center[1] + ft_radius * np.sin(angle)
        ft_upper_points_x.append(x)
        ft_upper_points_y.append(y)
    
    shapes.append(dict(
        type='path',
        path=' '.join([f"{'M' if i == 0 else 'L'} {x} {y}" for i, (x, y) in enumerate(zip(ft_upper_points_x, ft_upper_points_y))]),
        line=dict(color=court_color, width=line_width)
    ))
    
    # Semicircunferencia inferior (línea punteada)
    ft_lower_points_x = []
    ft_lower_points_y = []
    for angle in np.linspace(np.pi, 2*np.pi, 30):
        x = ft_center[0] + ft_radius * np.cos(angle)
        y = ft_center[1] + ft_radius * np.sin(angle)
        ft_lower_points_x.append(x)
        ft_lower_points_y.append(y)
    
    shapes.append(dict(
        type='path',
        path=' '.join([f"{'M' if i == 0 else 'L'} {x} {y}" for i, (x, y) in enumerate(zip(ft_lower_points_x, ft_lower_points_y))]),
        line=dict(color=court_color, width=line_width, dash='dash')
    ))
    
    # === ÁREA RESTRINGIDA ===
    # Generar puntos para semicircunferencia del área restringida
    restricted_radius = 40
    restricted_points_x = []
    restricted_points_y = []
    
    for angle in np.linspace(0, np.pi, 20):
        x = restricted_radius * np.cos(angle)
        y = restricted_radius * np.sin(angle)
        restricted_points_x.append(x)
        restricted_points_y.append(y)
    
    shapes.append(dict(
        type='path',
        path=' '.join([f"{'M' if i == 0 else 'L'} {x} {y}" for i, (x, y) in enumerate(zip(restricted_points_x, restricted_points_y))]),
        line=dict(color=court_color, width=line_width)
    ))
    
    # === LÍNEA DE 3 PUNTOS ===
    # Calcular los puntos donde el arco se conecta con las líneas rectas
    three_pt_radius = 237.5
    corner_y = 92.5  # Altura donde terminan las líneas de las esquinas
    
    # Esquinas izquierda y derecha
    shapes.append(dict(
        type='line',
        x0=-220, y0=-47.5, x1=-220, y1=corner_y,
        line=dict(color='#E67E22', width=line_width + 1)  # Naranja para línea de 3
    ))
    shapes.append(dict(
        type='line',
        x0=220, y0=-47.5, x1=220, y1=corner_y,
        line=dict(color='#E67E22', width=line_width + 1)
    ))
    
    # Arco de 3 puntos - usando múltiples puntos para crear el arco
    three_pt_points_x = []
    three_pt_points_y = []
    
    # Generar puntos del arco desde -220 hasta 220 en X
    for angle in np.linspace(-np.arcsin(corner_y/three_pt_radius), np.arcsin(corner_y/three_pt_radius), 50):
        x = three_pt_radius * np.sin(angle)
        y = three_pt_radius * np.cos(angle)
        three_pt_points_x.append(x)
        three_pt_points_y.append(y)
    
    # Añadir el arco como una línea que conecta todos los puntos
    shapes.append(dict(
        type='path',
        path=' '.join([f"{'M' if i == 0 else 'L'} {x} {y}" for i, (x, y) in enumerate(zip(three_pt_points_x, three_pt_points_y))]),
        line=dict(color='#E67E22', width=line_width + 1)
    ))
    
    # === CENTRO DE CANCHA ===
    # Semicircunferencia exterior del centro
    center_outer_points_x = []
    center_outer_points_y = []
    center_y = 422.5
    
    for angle in np.linspace(np.pi, 2*np.pi, 30):
        x = 60 * np.cos(angle)
        y = center_y + 60 * np.sin(angle)
        center_outer_points_x.append(x)
        center_outer_points_y.append(y)
    
    shapes.append(dict(
        type='path',
        path=' '.join([f"{'M' if i == 0 else 'L'} {x} {y}" for i, (x, y) in enumerate(zip(center_outer_points_x, center_outer_points_y))]),
        line=dict(color=court_color, width=line_width)
    ))
    
    # Semicircunferencia interior del centro
    center_inner_points_x = []
    center_inner_points_y = []
    
    for angle in np.linspace(np.pi, 2*np.pi, 20):
        x = 20 * np.cos(angle)
        y = center_y + 20 * np.sin(angle)
        center_inner_points_x.append(x)
        center_inner_points_y.append(y)
    
    shapes.append(dict(
        type='path',
        path=' '.join([f"{'M' if i == 0 else 'L'} {x} {y}" for i, (x, y) in enumerate(zip(center_inner_points_x, center_inner_points_y))]),
        line=dict(color=court_color, width=line_width)
    ))
    
    # === LÍNEAS EXTERIORES ===
    # Línea de fondo
    shapes.append(dict(
        type='line',
        x0=-250, y0=-47.5, x1=250, y1=-47.5,
        line=dict(color=court_color, width=line_width)
    ))
    # Líneas laterales
    shapes.append(dict(
        type='line',
        x0=-250, y0=-47.5, x1=-250, y1=422.5,
        line=dict(color=court_color, width=line_width)
    ))
    shapes.append(dict(
        type='line',
        x0=250, y0=-47.5, x1=250, y1=422.5,
        line=dict(color=court_color, width=line_width)
    ))

    fig.update_layout(shapes=shapes)
    return fig

def calculate_shot_zones(data):
    """Calcula estadísticas por zonas de tiro."""
    zones = {
        'Pintura': 0,
        'Tiros libres': 0,
        'Triples': 0,
        'Medio rango': 0
    }
    
    for _, shot in data.iterrows():
        x, y = shot['LOC_X'], shot['LOC_Y']
        distance = math.sqrt(x**2 + y**2)
        
        # Clasificar por zona
        if abs(x) <= 80 and y <= 142.5:  # Pintura
            zones['Pintura'] += 1
        elif distance > 237.5:  # Triples
            zones['Triples'] += 1
        elif y > 142.5 and y < 200:  # Zona de tiros libres
            zones['Tiros libres'] += 1
        else:  # Medio rango
            zones['Medio rango'] += 1
    
    return zones

def plot_shot_chart(data, title="Shot Chart"):
    """
    Crea un shot chart mejorado usando Plotly con mejor visualización.
    Nota: Los datos solo incluyen tiros anotados.
    """
    
    # Crear figura
    fig = go.Figure()
    
    if data is not None and not data.empty:
        # Calcular distancia para cada tiro
        data = data.copy()
        data['DISTANCE'] = np.sqrt(data['LOC_X']**2 + data['LOC_Y']**2)
        
        # Clasificar tiros por tipo
        paint_shots = data[(abs(data['LOC_X']) <= 80) & (data['LOC_Y'] <= 142.5)]
        three_pt_shots = data[data['DISTANCE'] > 237.5]
        mid_range_shots = data[(data['DISTANCE'] <= 237.5) & 
                              ~((abs(data['LOC_X']) <= 80) & (data['LOC_Y'] <= 142.5))]
        
        # Añadir tiros por categoría con diferentes colores y tamaños
        if not paint_shots.empty:
            fig.add_trace(go.Scatter(
                x=paint_shots['LOC_X'],
                y=paint_shots['LOC_Y'],
                mode='markers',
                name='Pintura',
                marker=dict(
                    color='#27AE60',  # Verde
                    size=12,
                    line=dict(color='white', width=2),
                    opacity=0.8,
                    symbol='circle'
                ),
                hovertemplate='<b>Tiro en la Pintura</b><br>' +
                             'Distancia: %{customdata:.1f} pies<br>' +
                             '<extra></extra>',
                customdata=paint_shots['DISTANCE'] / 10,
                showlegend=True
            ))
        
        if not three_pt_shots.empty:
            fig.add_trace(go.Scatter(
                x=three_pt_shots['LOC_X'],
                y=three_pt_shots['LOC_Y'],
                mode='markers',
                name='Triples',
                marker=dict(
                    color='#E74C3C',  # Rojo
                    size=14,
                    line=dict(color='white', width=2),
                    opacity=0.8,
                    symbol='star'
                ),
                hovertemplate='<b>Triple Anotado</b><br>' +
                             'Distancia: %{customdata:.1f} pies<br>' +
                             '<extra></extra>',
                customdata=three_pt_shots['DISTANCE'] / 10,
                showlegend=True
            ))
        
        if not mid_range_shots.empty:
            fig.add_trace(go.Scatter(
                x=mid_range_shots['LOC_X'],
                y=mid_range_shots['LOC_Y'],
                mode='markers',
                name='Medio Rango',
                marker=dict(
                    color='#3498DB',  # Azul
                    size=10,
                    line=dict(color='white', width=2),
                    opacity=0.8,
                    symbol='diamond'
                ),
                hovertemplate='<b>Tiro de Medio Rango</b><br>' +
                             'Distancia: %{customdata:.1f} pies<br>' +
                             '<extra></extra>',
                customdata=mid_range_shots['DISTANCE'] / 10,
                showlegend=True
            ))
        
        # Calcular estadísticas
        total_shots = len(data)
        zones = calculate_shot_zones(data)
        
        # Crear título dinámico con estadísticas
        title = f"🏀 {title}<br><sub>Total de Canastas: {total_shots} | " + \
                f"Pintura: {zones['Pintura']} | Triples: {zones['Triples']} | " + \
                f"Medio Rango: {zones['Medio rango']}</sub>"
    
    # Añadir la cancha
    fig = add_court_shapes(fig)
    
    # Layout mejorado
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=20, color='#2C3E50', family='Arial Black')
        ),
        xaxis=dict(
            range=[-260, 260],
            visible=False,
            scaleanchor="y",
            scaleratio=1
        ),
        yaxis=dict(
            range=[-60, 440],
            visible=False
        ),
        height=700,
        width=600,
        plot_bgcolor='#F8F9FA',  # Fondo gris claro
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1,
            font=dict(size=12)
        ),
        margin=dict(l=20, r=20, t=80, b=60),
    )
    
    # Configurar aspectos para mantener proporciones de cancha real
    fig.update_xaxes(constrain='domain')
    fig.update_yaxes(constrain='domain')
    
    return fig