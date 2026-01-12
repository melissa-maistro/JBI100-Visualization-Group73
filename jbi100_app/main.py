from dash import Dash, html, dcc, ctx, no_update
from dash.dependencies import Input, Output, State
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.map import MapView
from jbi100_app.views.radar import RadarView
from jbi100_app.views.compare import CompareView
from jbi100_app.data import get_data

app = Dash(__name__)
app.title = "Humanitarian Risk Viz"

# Caricamento dati
df = get_data()

# Inizializzazione Viste
map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)
compare_view = CompareView("Compare View", df)

# --- STILI CSS ---
DRAWER_STYLE = {
    "position": "fixed",
    "top": "80px",
    "backgroundColor": "white",
    "borderRadius": "12px",
    "boxShadow": "0 4px 20px rgba(0,0,0,0.15)",
    # Deve stare sopra hamburger (z-index: 2000) e sopra la mappa
    "zIndex": 2500,
    "padding": "20px",
    "transition": "transform 0.4s ease-in-out",

    # La pagina è overflow:hidden (style.css). Quindi il drawer deve scrollare.
    "maxHeight": "85vh",
    "overflowY": "auto",
    "overflowX": "visible",
}

app.layout = html.Div([
    dcc.Store(id='menu-open', data=False),
    dcc.Store(id='compare-mode-active', data=False),

    # 1. MENU SINISTRO (Filtri + Tasto Compare)
    html.Div(
        id="menu-drawer",
        style={**DRAWER_STYLE, "left": "80px", "width": "300px", "transform": "translateX(-120%)"},
        children=[
            make_menu_layout(),
            html.Hr(),
            html.H5("Comparison Task"),
            html.Button("Activate Compare Mode", id="toggle-compare-btn", className="btn-action"),

            # Area controlli comparazione
            html.Div(
                id="compare-controls-area",
                style={"display": "none", "marginTop": "15px"},
                children=[
                    html.Label("Choose Countries:", style={"fontSize": "13px"}),
                    dcc.Dropdown(
                        id="compare-dropdown",
                        options=[{'label': c, 'value': c} for c in sorted(df['Country'].unique())],
                        multi=True,
                        placeholder="Select items...",
                        # mantiene il dropdown sopra la mappa
                        style={"position": "relative", "zIndex": 3000}
                    ),
                    html.Button(
                        "Confirm Comparison",
                        id="confirm-compare-btn",
                        className="btn-confirm",
                        style={"marginTop": "15px"}
                    )
                ]
            )
        ]
    ),

    # 2. PARALLEL PLOT (Esce da SINISTRA)
    html.Div(
        id="parallel-drawer",
        style={**DRAWER_STYLE, "left": "80px", "width": "650px", "transform": "translateX(-120%)", "zIndex": 2600},
        children=[
            html.Div([
                html.H4("Global Comparison", style={"display": "inline-block", "margin": 0}),
                html.Button("×", id="close-parallel-btn", className="close-btn", style={"float": "right"})
            ], style={"marginBottom": "15px"}),
            compare_view
        ]
    ),

    # 3. RADAR DRAWER (Esce da DESTRA)
    html.Div(
        id="radar-drawer",
        style={**DRAWER_STYLE, "right": "20px", "width": "420px", "transform": "translateX(120%)"},
        children=[
            html.Div([
                html.Button("×", id="close-radar-btn", className="close-btn", style={"float": "right"}),
                html.H4("Country Profile", style={"textAlign": "center", "margin": 0})
            ], style={"marginBottom": "15px"}),
            radar_view
        ]
    ),

    # BOTTONI FISSI
    html.Button("☰", id="hamburger-btn", className="floating-btn", style={"left": "20px"}),

    # Zoom +/-
    html.Div([
        html.Button("+", id="zoom-in-map", className="zoom-btn"),
        html.Button("-", id="zoom-out-map", className="zoom-btn"),
    ], style={"position": "fixed", "bottom": "30px", "left": "30px", "zIndex": 1200, "display": "flex", "flexDirection": "column"}),

    # MAPPA
    html.Div(map_view, id="map-parent")
])

# --- CALLBACKS ---

# A. Toggle Menu Principale
@app.callback(
    [Output("menu-drawer", "style"), Output("menu-open", "data")],
    Input("hamburger-btn", "n_clicks"),
    State("menu-open", "data"),
    prevent_initial_call=True
)
def toggle_menu(n, is_open):
    new_state = not is_open
    transform = "translateX(0)" if new_state else "translateX(-120%)"
    style = {**DRAWER_STYLE, "left": "80px", "width": "300px", "transform": transform}
    return style, new_state

# B. Toggle UI Comparazione
@app.callback(
    [Output("compare-controls-area", "style"), Output("compare-mode-active", "data"), Output("toggle-compare-btn", "children")],
    Input("toggle-compare-btn", "n_clicks"),
    State("compare-mode-active", "data"),
    prevent_initial_call=True
)
def toggle_compare_mode(n, active):
    new_active = not active
    display = {"display": "block"} if new_active else {"display": "none"}
    label = "Deactivate Compare Mode" if new_active else "Activate Compare Mode"
    return display, new_active, label

# C. Gestione Radar (Task 1) - Destra
@app.callback(
    [Output("radar-drawer", "style"), Output(radar_view.html_id, "figure")],
    [Input(map_view.html_id, "clickData"), Input("close-radar-btn", "n_clicks")],
    State("compare-mode-active", "data"),
    prevent_initial_call=True
)
def handle_radar(click_data, close_n, compare_active):
    ctx_id = ctx.triggered_id

    # Se clicco X o se attivo la modalità compare, chiudi radar
    if ctx_id == "close-radar-btn" or compare_active:
        return {**DRAWER_STYLE, "right": "20px", "width": "420px", "transform": "translateX(120%)"}, no_update

    # Se clicco un paese sulla mappa e NON sono in compare mode, apri radar
    if click_data:
        country = click_data['points'][0]['location']
        return {**DRAWER_STYLE, "right": "20px", "width": "420px", "transform": "translateX(0)"}, radar_view.update(country)

    return no_update, no_update

# D. Gestione Comparazione (Task 2) - Sinistra
@app.callback(
    [Output("parallel-drawer", "style"),
     Output(compare_view.html_id, "figure"),
     Output(map_view.html_id, "figure")],
    [Input("confirm-compare-btn", "n_clicks"),
     Input("close-parallel-btn", "n_clicks"),
     Input("select-risk-variable", "value"),
     Input("compare-dropdown", "value")],
    prevent_initial_call=True
)
def handle_comparison(n_confirm, n_close, risk, countries):
    ctx_id = ctx.triggered_id

    # Aggiorna sempre la mappa per evidenziare i paesi selezionati (bordi neri)
    safe_countries = countries if countries else []
    map_fig = map_view.update(risk, safe_countries)

    # Se clicco conferma E ho paesi selezionati -> Apri drawer
    if ctx_id == "confirm-compare-btn" and safe_countries:
        fig_comp = compare_view.update(safe_countries)
        style = {**DRAWER_STYLE, "left": "80px", "width": "650px", "transform": "translateX(0)", "zIndex": 2600}
        return style, fig_comp, map_fig

    # Se clicco X -> Chiudi drawer ma mantieni mappa aggiornata
    if ctx_id == "close-parallel-btn":
        style = {**DRAWER_STYLE, "left": "80px", "width": "650px", "transform": "translateX(-120%)"}
        return style, no_update, map_fig

    # Per qualsiasi altro input (es. cambio dropdown), aggiorna solo mappa
    return no_update, no_update, map_fig

if __name__ == '__main__':
    app.run_server(debug=True)