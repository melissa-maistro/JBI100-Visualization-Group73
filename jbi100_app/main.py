from dash import Dash, html
from dash.dependencies import Input, Output
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.map import MapView
from jbi100_app.views.radar import RadarView
from jbi100_app.data import get_data

# Inizializza l'app
app = Dash(__name__)
app.title = "Humanitarian Risk Viz"

# Carica dati puliti
df = get_data()

# Istanzia le visualizzazioni (Classi definite nei file views/)
map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)

# Definisci il Layout
app.layout = html.Div(
    id="app-container",
    children=[
        # Colonna Sinistra: Menu
        html.Div(
            id="left-column",
            className="three columns",
            children=make_menu_layout()
        ),

        # Colonna Destra: Visualizzazioni
        html.Div(
            id="right-column",
            className="nine columns",
            children=[
                html.H3("Global Risk Distribution"),
                # La Mappa
                map_view, 
                html.Hr(), # Linea separatrice
                # Il Radar
                radar_view
            ],
        ),
    ],
)

# --- CALLBACKS ---
# Le callback collegano gli input (menu, click) agli output (grafici)

# 1. Aggiorna la Mappa quando cambi il Rischio nel Menu
@app.callback(
    Output(map_view.html_id, "figure"),
    Input("select-risk-variable", "value") # Assicurati che l'ID nel menu.py sia questo
)
def update_map_callback(selected_risk):
    return map_view.update(selected_risk)

# 2. Aggiorna il Radar quando clicchi sulla Mappa
@app.callback(
    Output(radar_view.html_id, "figure"),
    Input(map_view.html_id, "clickData")
)
def update_radar_callback(click_data):
    selected_country = None
    if click_data:
        selected_country = click_data['points'][0]['location']
    return radar_view.update(selected_country)