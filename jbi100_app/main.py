from dash import Dash, html, ctx
from dash.dependencies import Input, Output
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.map import MapView
from jbi100_app.views.radar import RadarView
from jbi100_app.data import get_data

app = Dash(__name__)
app.title = "JBI100 Humanitarian Viz"

# 1. Carica i dati
df = get_data()

# 2. Istanzia le viste
map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)

# 3. Definisci il Layout
app.layout = html.Div(
    id="app-container",
    children=[
        # Sinistra: Menu
        make_menu_layout(),
        
        # Destra: Visualizzazioni
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Mappa in alto
                html.Div(map_view),
                # Radar in basso
                html.Div(radar_view)
            ],
        ),
    ],
)

# 4. Callback
# Aggiorna Mappa quando cambia il Dropdown
@app.callback(
    Output(map_view.html_id, "figure"),
    Input("select-risk-variable", "value")
)
def update_map(selected_variable):
    return map_view.update(selected_variable)

# Aggiorna Radar quando si clicca sulla Mappa
@app.callback(
    Output(radar_view.html_id, "figure"),
    Input(map_view.html_id, "clickData")
)
def update_radar(click_data):
    selected_country = None
    if click_data:
        selected_country = click_data['points'][0]['location']
    return radar_view.update(selected_country)