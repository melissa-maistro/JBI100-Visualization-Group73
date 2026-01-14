from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output, State
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.map import MapView
from jbi100_app.views.radar import RadarView
from jbi100_app.views.compare import CompareView  # <--- NUOVO IMPORT
from jbi100_app.data import get_data
import dash

app = Dash(__name__)
app.title = "Humanitarian Risk Viz"

# Caricamento dati e Viste
df = get_data()
map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)
compare_view = CompareView("Compare View", df)  # <--- ISTANZA COMPARE VIEW

# Lista paesi per il dropdown
all_countries = sorted(df['Country'].unique().tolist())

# --- STILI CSS ---

# 1. Stile del Menu (Drawer laterale)
MENU_CONTAINER_STYLE = {
    "position": "fixed", "top": "80px", "left": "20px", "zIndex": 2000,
    "width": "fit-content", "height": "auto", "maxHeight": "85vh",
    "overflow": "visible", "opacity": 0, "visibility": "hidden",
    "transition": "opacity 0.3s ease-in-out, visibility 0.3s ease-in-out",
    "display": "block"
}

# 2. Stile della Finestra RADAR
RADAR_CONTAINER_STYLE = {
    "position": "fixed", "top": "100px", "left": "100px",
    "width": "400px", "height": "auto", "maxHeight": "80vh",
    "backgroundColor": "white", "borderRadius": "12px",
    "boxShadow": "0 10px 30px rgba(0,0,0,0.3)", "zIndex": 1000,
    "padding": "20px", "display": "none", "flexDirection": "column",
    "cursor": "default"
}

# 3. Bottone Hamburger
HAMBURGER_STYLE = {
    "position": "fixed", "top": "20px", "left": "20px", "zIndex": 2100,
    "backgroundColor": "white", "border": "none", "borderRadius": "50%",
    "width": "50px", "height": "50px", "display": "flex",
    "alignItems": "center", "justifyContent": "center", "cursor": "pointer",
    "fontSize": "24px", "boxShadow": "0 4px 10px rgba(0,0,0,0.2)", "color": "#333"
}

# 4. Backdrop
BACKDROP_STYLE = {
    "position": "fixed", "top": 0, "left": 0, "width": "100vw", "height": "100vh",
    "backgroundColor": "rgba(0,0,0,0.5)", "zIndex": 1900, "display": "none",
    "backdropFilter": "blur(3px)"
}

# 5. Stile Tasti Zoom
ZOOM_CONTAINER_STYLE = {
    "position": "fixed", "bottom": "30px", "right": "30px", "zIndex": 1000,
    "display": "flex", "flexDirection": "column",
    "boxShadow": "0 2px 6px rgba(0,0,0,0.3)", "borderRadius": "4px",
    "overflow": "hidden", "backgroundColor": "white"
}

ZOOM_BTN_STYLE = {
    "width": "40px", "height": "40px", "backgroundColor": "white", "border": "none",
    "borderBottom": "1px solid #eee", "cursor": "pointer", "fontSize": "20px",
    "fontWeight": "bold", "color": "#555", "display": "flex",
    "alignItems": "center", "justifyContent": "center"
}

# --- NUOVI STILI PER COMPARE MODE ---
COMPARE_BTN_STYLE = {
    "position": "fixed",
    "top": "25px",              # Allineato con l'hamburger
    "left": "90px",             # Subito a destra dell'hamburger
    "zIndex": 2100,
    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", # Gradiente carino
    "color": "white",
    "border": "none",
    "padding": "10px 25px",
    "borderRadius": "50px",     # Forma a pillola
    "cursor": "pointer",
    "boxShadow": "0 4px 15px rgba(0,0,0,0.2)",
    "fontWeight": "bold",
    "fontSize": "14px",
    "letterSpacing": "0.5px",
    "transition": "transform 0.2s, box-shadow 0.2s",
    "textTransform": "uppercase"
}


COMPARE_PANEL_STYLE = {
    "position": "fixed",
    "top": "80px",              # Sotto il bottone
    "left": "90px",             # Allineato a sinistra col bottone
    "zIndex": 2000,
    "width": "280px",
    "backgroundColor": "white",
    "borderRadius": "12px",
    "padding": "15px",
    "boxShadow": "0 8px 30px rgba(0,0,0,0.15)",
    "display": "none",
    "border": "1px solid #eee"
}


COMPARE_DRAWER_STYLE = {
    "position": "fixed",
    "bottom": "0",
    "left": "0",
    "width": "100vw",
    "height": "230px",          # <--- RIDOTTO (Era 320px)
    "backgroundColor": "white",
    "zIndex": 1500,
    "boxShadow": "0 -5px 20px rgba(0,0,0,0.1)",
    "borderTopLeftRadius": "20px",
    "borderTopRightRadius": "20px",
    "padding": "15px 30px",     # Più padding laterale
    "display": "none",
    "transition": "transform 0.3s ease-in-out",
    "boxSizing": "border-box"   # Importante per il padding
}


# --- LAYOUT ---
app.layout = html.Div([
    dcc.Store(id='menu-state-store', data=False),
    dcc.Store(id='radar-state-store', data=False),
    
    # NUOVI STORE PER COMPARE
    dcc.Store(id='compare-mode-store', data=False),  # True/False
    dcc.Store(id='selected-countries-store', data=[]),  # Lista paesi selezionati

    # Elementi Menu Esistenti
    html.Button("☰", id="hamburger-btn", n_clicks=0, style=HAMBURGER_STYLE),
    html.Div(id="menu-backdrop", style=BACKDROP_STYLE, n_clicks=0),
    html.Div(id="menu-drawer", style=MENU_CONTAINER_STYLE,
             children=[html.Div(make_menu_layout(), style={"minWidth": "300px"})]),

    # --- NUOVI ELEMENTI COMPARE ---
    html.Button("Compare Countries", id="compare-btn", n_clicks=0, style=COMPARE_BTN_STYLE),

    # Pannello Ricerca (Sotto il bottone Compare)
    html.Div(id="compare-search-panel", style=COMPARE_PANEL_STYLE, children=[
        html.Label("Search or Click on Map:", style={"fontSize": "12px", "color": "#555"}),
        dcc.Dropdown(
            id="country-selector",
            options=[{'label': c, 'value': c} for c in all_countries],
            multi=True,
            placeholder="Select countries...",
            style={"fontSize": "13px"}
        )
    ]),

    # Drawer Inferiore (Grafico Comparazione)
    html.Div(id="compare-drawer", style=COMPARE_DRAWER_STYLE, children=[
        html.Button("×", id="close-compare-btn", n_clicks=0,
                    style={"float": "right", "border": "none", "background": "transparent", "fontSize": "20px", "cursor": "pointer"}),
        html.Div(compare_view, style={"height": "100%", "width": "100%", "marginTop": "-20px"})
    ]),
    # ------------------------------

    # Radar Drawer (Esistente)
    html.Div(id="radar-drawer", style=RADAR_CONTAINER_STYLE, children=[
        html.Div(id="radar-header",
            style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "15px", "padding": "10px", "cursor": "move", "backgroundColor": "#f9f9f9", "borderBottom": "1px solid #eee", "borderRadius": "12px 12px 0 0"},
            children=[
                html.H5("Country Details", style={"margin": 0, "userSelect": "none"}),
                html.Button("×", id="close-radar-btn", n_clicks=0, style={"border": "none", "background": "transparent", "fontSize": "20px", "cursor": "pointer"})
            ]
        ),
        html.Div(radar_view, style={"flex": "1", "padding": "0 10px"})
    ]),

    # Tasti Zoom
    html.Div(style=ZOOM_CONTAINER_STYLE, children=[
        html.Button("+", id="btn-zoom-in", n_clicks=0, style=ZOOM_BTN_STYLE),
        html.Button("-", id="btn-zoom-out", n_clicks=0, style={**ZOOM_BTN_STYLE, "borderBottom": "none"})
    ]),

    # Mappa Fullscreen
    html.Div(
        style={"height": "100vh", "width": "100vw", "position": "absolute", "top": 0, "left": 0, "zIndex": 1},
        children=[map_view]
    )
])


# --- CALLBACKS ---

# A. Menu Logic (Esistente)
@app.callback(
    Output("menu-state-store", "data"),
    [Input("hamburger-btn", "n_clicks"), Input("menu-backdrop", "n_clicks"), Input("select-risk-variable", "value")],
    [State("menu-state-store", "data")]
)
def update_menu_state(n_hamburger, n_backdrop, risk_value, is_open):
    trigger = ctx.triggered_id
    if not trigger: return False
    if trigger == "select-risk-variable": return False
    if trigger == "hamburger-btn": return not is_open
    if trigger == "menu-backdrop": return False
    return is_open

@app.callback(
    [Output("menu-drawer", "style"), Output("menu-backdrop", "style")],
    Input("menu-state-store", "data")
)
def update_menu_visuals(is_open):
    drawer_style = MENU_CONTAINER_STYLE.copy()
    backdrop_style = BACKDROP_STYLE.copy()
    if is_open:
        drawer_style.update({"opacity": 1, "visibility": "visible", "transform": "translateY(0)"})
        backdrop_style["display"] = "block"
    else:
        drawer_style.update({"opacity": 0, "visibility": "hidden", "transform": "translateY(-10px)"})
        backdrop_style["display"] = "none"
    return drawer_style, backdrop_style


# --- NUOVA LOGICA: COMPARE MODE ---

# B1. Toggle Compare Mode (Attiva/Disattiva Interfaccia)
@app.callback(
    [Output("compare-mode-store", "data"),
     Output("compare-search-panel", "style"),
     Output("compare-drawer", "style"),
     Output("compare-btn", "style"),
     Output("compare-btn", "children"),
     Output("selected-countries-store", "data")], # Reset selezione alla chiusura
    [Input("compare-btn", "n_clicks"),
     Input("close-compare-btn", "n_clicks")],
    [State("compare-mode-store", "data")]
)

def toggle_compare_mode(btn_click, close_click, is_active):
    trigger = ctx.triggered_id
    if not trigger: return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Determina nuovo stato
    new_state = not is_active if trigger == "compare-btn" else False
    
    search_style = COMPARE_PANEL_STYLE.copy()
    drawer_style = COMPARE_DRAWER_STYLE.copy()
    btn_style = COMPARE_BTN_STYLE.copy()

    if new_state:
        search_style["display"] = "block"
        drawer_style["display"] = "block"
        btn_style["backgroundColor"] = "#e74c3c" # Rosso per indicare stato attivo
        return True, search_style, drawer_style, btn_style, "Stop Comparing", dash.no_update
    else:
        search_style["display"] = "none"
        drawer_style["display"] = "none"
        btn_style["backgroundColor"] = "#2c3e50"
        # Reset lista selezione ([]), Reset Button text
        return False, search_style, drawer_style, btn_style, "Compare Countries", []


# B2. Gestione Selezione (Unisci Mappa e Dropdown)
@app.callback(
    Output("country-selector", "value"),
    [Input(map_view.html_id, "clickData"),
     Input("country-selector", "value")],
    [State("compare-mode-store", "data")]
)
def manage_selection_ui(map_click, dropdown_value, compare_mode):
    trigger = ctx.triggered_id
    
    # Se non siamo in modalità compare, ignora i click mappa per la selezione
    if not compare_mode and trigger == map_view.html_id:
        return dash.no_update

    # Se trigger è Dropdown -> È la fonte di verità, ritorna se stesso (no-op visuale)
    if trigger == "country-selector":
        return dropdown_value

    # Se trigger è Mappa -> Aggiungi/Rimuovi paese dalla lista attuale
    if trigger == map_view.html_id and map_click:
        clicked_country = map_click['points'][0]['location']
        current_list = dropdown_value or []
        
        if clicked_country in current_list:
            new_list = [c for c in current_list if c != clicked_country]
        else:
            new_list = current_list + [clicked_country]
        
        return new_list

    return dash.no_update

# B3. Sync Dropdown UI -> Data Store
@app.callback(
    Output("selected-countries-store", "data", allow_duplicate=True),
    Input("country-selector", "value"),
    prevent_initial_call=True
)
def sync_store(value):
    return value or []

# B4. Aggiorna Grafico Compare
@app.callback(
    Output(compare_view.html_id, "figure"),
    Input("selected-countries-store", "data")
)
def update_compare_view(selected_countries):
    return compare_view.update(selected_countries)


# --- LOGICA VISIBILITÀ RADAR (MODIFICATA) ---

@app.callback(
    [Output("radar-state-store", "data"),
     Output(map_view.html_id, "clickData")],
    [Input(map_view.html_id, "clickData"),
     Input("close-radar-btn", "n_clicks")],
    [State("radar-state-store", "data"),
     State("compare-mode-store", "data")] # Controlla se siamo in compare mode
)
def toggle_radar_visibility(map_click, close_click, is_open, is_compare_mode):
    trigger = ctx.triggered_id
    if not trigger: return is_open, dash.no_update

    # SE COMPARE MODE È ATTIVA -> IL RADAR RIMANE CHIUSO
    if is_compare_mode:
        return False, None # Chiudi radar se aperto, non resettare click (serve per selezione)

    if trigger == "close-radar-btn":
        return False, None

    if trigger == map_view.html_id and map_click:
        return True, dash.no_update

    return is_open, dash.no_update

@app.callback(
    Output("radar-drawer", "style"),
    Input("radar-state-store", "data"),
    State("radar-drawer", "style")
)
def update_radar_visuals(is_open, current_style):
    if current_style is None: current_style = RADAR_CONTAINER_STYLE.copy()
    new_style = current_style.copy()
    if is_open:
        new_style["display"] = "flex"
        new_style["transform"] = "none"
    else:
        new_style["display"] = "none"
    return new_style


# --- AGGIORNAMENTO MAPPA E RADAR ---

@app.callback(
    Output(map_view.html_id, "figure"),
    [Input("select-risk-variable", "value"),
     Input("selected-countries-store", "data")] # Ora ascolta anche la lista selezione
)
def update_map(selected_risk, selected_countries):
    # Passiamo entrambi gli argomenti al metodo update della mappa
    return map_view.update(selected_risk, selected_countries)

@app.callback(
    Output(radar_view.html_id, "figure"),
    [Input(map_view.html_id, "clickData"),
     Input("select-risk-variable", "value")]
)
def update_radar_data(click_data, selected_risk):
    country = click_data['points'][0]['location'] if click_data else None
    return radar_view.update(country, selected_risk)


# --- INFO WINDOW (Esistente) ---
@app.callback(
    [Output("info-card", "style"), Output("info-backdrop", "style")],
    [Input("open-info-btn", "n_clicks"), Input("info-backdrop", "n_clicks")],
    [State("info-card", "style"), State("info-backdrop", "style")],
    prevent_initial_call=True
)
def toggle_info_window(btn_clicks, backdrop_clicks, card_style, backdrop_style):
    if card_style is None: card_style = {}
    if backdrop_style is None: backdrop_style = {}
    ctx_id = ctx.triggered_id
    new_card, new_backdrop = card_style.copy(), backdrop_style.copy()
    is_visible = new_card.get('display', 'none') == 'block'

    if ctx_id == "open-info-btn":
        if not is_visible:
            new_card['display'] = 'block'; new_backdrop['display'] = 'block'
        else:
            new_card['display'] = 'none'; new_backdrop['display'] = 'none'
    elif ctx_id == "info-backdrop":
        new_card['display'] = 'none'; new_backdrop['display'] = 'none'

    return new_card, new_backdrop


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)