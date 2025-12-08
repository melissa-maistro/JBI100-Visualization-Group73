from dash import Dash, html
from dash.dependencies import Input, Output
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.map import MapView
from jbi100_app.views.radar import RadarView
from jbi100_app.data import get_data

# Inizializza l'app
app = Dash(__name__)
app.title = "Humanitarian Risk Viz"

# 1. Carica i dati
df = get_data()

# 2. Crea le istanze delle viste
map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)

# 3. Definisci il Layout (CSS Grid-like)
app.layout = html.Div(
    id="app-container",
    children=[
        # Sinistra: Menu
        make_menu_layout(),
        
        # Destra: Area Visualizzazioni
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Riga in alto: Mappa
                html.Div(
                    children=[map_view],
                    style={'height': '60vh', 'marginBottom': '20px'}
                ),
                
                # Riga in basso: Radar (Dettaglio)
                html.Div(
                    children=[radar_view],
                    style={'height': '40vh'}
                )
            ],
        ),
    ],
)

# 4. Callbacks

# A. Aggiorna la Mappa quando cambi il Dropdown
@app.callback(
    Output(map_view.html_id, "figure"),
    Input("select-risk-variable", "value")
)
def update_map(selected_risk):
    return map_view.update(selected_risk)

# B. Aggiorna il Radar quando clicchi sulla Mappa
@app.callback(
    Output(radar_view.html_id, "figure"),
    Input(map_view.html_id, "clickData")
)
def update_radar(click_data):
    selected_country = None
    # Verifica se c'è un click
    if click_data:
        selected_country = click_data['points'][0]['location']
    
    # Se non c'è click, passa None (la vista mostrerà la media globale)
    return radar_view.update(selected_country)