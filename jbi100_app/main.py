from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output, State
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.map import MapView
from jbi100_app.views.radar import RadarView
from jbi100_app.data import get_data
import dash

app = Dash(__name__)
app.title = "Humanitarian Risk Viz"

df = get_data()
map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)

# --- STILI CSS ---

# 1. Stile del Menu (Drawer laterale invisibile/contenitore)
MENU_CONTAINER_STYLE = {
    "position": "fixed",
    "top": "80px",
    "left": "20px",
    "zIndex": 2000,
    "width": "fit-content",
    "height": "auto",
    "maxHeight": "85vh",
    "overflow": "visible",
    "opacity": 0,
    "visibility": "hidden",
    "transition": "opacity 0.3s ease-in-out, visibility 0.3s ease-in-out",
    "display": "block"
}

# 2. Stile della Finestra RADAR (Aggiornato per Drag & Drop)
RADAR_CONTAINER_STYLE = {
    "position": "fixed",
    "top": "100px",       # Posizione iniziale Y
    "left": "100px",      # Posizione iniziale X (non più right)
    "width": "400px",     # Larghezza fissa
    "height": "auto",
    "maxHeight": "80vh",
    "backgroundColor": "white",
    "borderRadius": "12px",
    "boxShadow": "0 10px 30px rgba(0,0,0,0.3)", # Ombra più profonda per effetto "flottante"
    "zIndex": 1000,
    "padding": "20px",
    "display": "none",    # Nascondiamo di default con display, non con transform
    "flexDirection": "column",
    "cursor": "default"
}

# 3. Bottone Hamburger
HAMBURGER_STYLE = {
    "position": "fixed",
    "top": "20px",
    "left": "20px",
    "zIndex": 2100,
    "backgroundColor": "white",
    "border": "none",
    "borderRadius": "50%",
    "width": "50px",
    "height": "50px",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "cursor": "pointer",
    "fontSize": "24px",
    "boxShadow": "0 4px 10px rgba(0,0,0,0.2)",
    "color": "#333"
}

# 4. Backdrop
BACKDROP_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "width": "100vw",
    "height": "100vh",
    "backgroundColor": "rgba(0,0,0,0.5)",
    "zIndex": 1900,
    "display": "none",
    "backdropFilter": "blur(3px)"
}
# --- STILE TASTI ZOOM ---
ZOOM_CONTAINER_STYLE = {
    "position": "fixed",
    "bottom": "30px",
    "right": "30px",
    "zIndex": 1000,
    "display": "flex",
    "flexDirection": "column",
    "boxShadow": "0 2px 6px rgba(0,0,0,0.3)",
    "borderRadius": "4px",
    "overflow": "hidden",
    "backgroundColor": "white"
}

ZOOM_BTN_STYLE = {
    "width": "40px",
    "height": "40px",
    "backgroundColor": "white",
    "border": "none",
    "borderBottom": "1px solid #eee",
    "cursor": "pointer",
    "fontSize": "20px",
    "fontWeight": "bold",
    "color": "#555",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center"
}

app.layout = html.Div([
    dcc.Store(id='menu-state-store', data=False),
    dcc.Store(id='radar-state-store', data=False),

    # Elementi UI
    html.Button("☰", id="hamburger-btn", n_clicks=0, style=HAMBURGER_STYLE),
    html.Div(id="menu-backdrop", style=BACKDROP_STYLE, n_clicks=0),

    # Menu Drawer
    html.Div(
        id="menu-drawer",
        style=MENU_CONTAINER_STYLE,
        children=[
            html.Div(
                children=[make_menu_layout()],
                style={"minWidth": "300px"}
            )
        ]
    ),

    # Radar Drawer
    html.Div(
        id="radar-drawer",
        style=RADAR_CONTAINER_STYLE,
        children=[
            # --- HEADER (Zona Trascinabile) ---
            html.Div(
                id="radar-header",  # <--- QUESTO ID È OBBLIGATORIO PER IL JS
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "15px",
                    "padding": "10px",
                    "cursor": "move",  # <--- Il cursore deve diventare una croce
                    "backgroundColor": "#f9f9f9",  # Un po' di colore per riconoscerlo
                    "borderBottom": "1px solid #eee",
                    "borderRadius": "12px 12px 0 0"
                },
                children=[
                    html.H5("Country Details", style={"margin": 0, "userSelect": "none"}),
                    html.Button(
                        "×",
                        id="close-radar-btn",
                        n_clicks=0,
                        style={"border": "none", "background": "transparent", "fontSize": "20px", "cursor": "pointer"}
                    )
                ]
            ),
            # Contenuto del Radar
            html.Div(radar_view, style={"flex": "1", "padding": "0 10px"})
        ]
    ),
    # NUOVI TASTI ZOOM
    html.Div(
        style=ZOOM_CONTAINER_STYLE,
        children=[
            html.Button("+", id="btn-zoom-in", n_clicks=0, style=ZOOM_BTN_STYLE),
            html.Button("-", id="btn-zoom-out", n_clicks=0, style={**ZOOM_BTN_STYLE, "borderBottom": "none"})
        ]
    ),
    # Mappa Fullscreen
    html.Div(
        style={
            "height": "100vh",
            "width": "100vw",
            "position": "absolute",
            "top": 0,
            "left": 0,
            "zIndex": 1
        },
        children=[map_view]
    )

])


# --- CALLBACKS ---

# A. Menu Logic
@app.callback(
    Output("menu-state-store", "data"),
    [Input("hamburger-btn", "n_clicks"),
     Input("menu-backdrop", "n_clicks"),
     Input("select-risk-variable", "value")],
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
    [Output("menu-drawer", "style"),
     Output("menu-backdrop", "style")],
    Input("menu-state-store", "data")
)
def update_menu_visuals(is_open):
    drawer_style = MENU_CONTAINER_STYLE.copy()
    backdrop_style = BACKDROP_STYLE.copy()

    if is_open:
        drawer_style["opacity"] = 1
        drawer_style["visibility"] = "visible"
        drawer_style["transform"] = "translateY(0)"
        backdrop_style["display"] = "block"
    else:
        drawer_style["opacity"] = 0
        drawer_style["visibility"] = "hidden"
        drawer_style["transform"] = "translateY(-10px)"
        backdrop_style["display"] = "none"

    return drawer_style, backdrop_style


# B. Radar Visibility Logic
@app.callback(
    [Output("radar-state-store", "data"),
     Output(map_view.html_id, "clickData")],  # <--- NUOVO OUTPUT: Resetta il click
    [Input(map_view.html_id, "clickData"),
     Input("close-radar-btn", "n_clicks")],
    [State("radar-state-store", "data")]
)
def toggle_radar_visibility(map_click, close_click, is_open):
    trigger = ctx.triggered_id

    # 1. Caricamento iniziale: non fare nulla
    if not trigger:
        return is_open, dash.no_update

    # 2. Se premo la X -> Chiudi finestra E dimentica il click
    if trigger == "close-radar-btn":
        # Output 1: False (chiudi), Output 2: None (resetta mappa)
        return False, None

    # 3. Se clicco sulla mappa -> Apri finestra
    if trigger == map_view.html_id and map_click:
        # Output 1: True (apri), Output 2: no_update (tieni il dato cliccato)
        return True, dash.no_update

    return is_open, dash.no_update

@app.callback(
    Output("radar-drawer", "style"),
    Input("radar-state-store", "data"),
    State("radar-drawer", "style")
)
def update_radar_visuals(is_open, current_style):
    if current_style is None:
        current_style = RADAR_CONTAINER_STYLE.copy()

    new_style = current_style.copy()

    if is_open:
        new_style["display"] = "flex"
        # IMPORTANTE: Rimuovi le catene!
        # Se c'è un transform attivo, la finestra sembra bloccata.
        new_style["transform"] = "none"
    else:
        new_style["display"] = "none"

    return new_style
# C. AGGIORNAMENTO DATI (Map & Radar)
@app.callback(
    Output(map_view.html_id, "figure"),
    Input("select-risk-variable", "value")
)
def update_map(selected_risk):
    return map_view.update(selected_risk)


# --- CORREZIONE QUI SOTTO ---
@app.callback(
    Output(radar_view.html_id, "figure"),
    [Input(map_view.html_id, "clickData"),
     Input("select-risk-variable", "value")]  # <--- ORA ASCOLTA ANCHE IL MENU
)
def update_radar_data(click_data, selected_risk):
    # Recupera il paese cliccato (se esiste)
    country = click_data['points'][0]['location'] if click_data else None

    # Passa SIA il paese SIA il rischio selezionato alla vista Radar
    # Nota: Assicurati che radar.py accetti due argomenti in update()
    return radar_view.update(country, selected_risk)


# --- CALLBACK PER INFO WINDOW (ROBUSTA) ---
@app.callback(
    [Output("info-card", "style"),
     Output("info-backdrop", "style")],
    [Input("open-info-btn", "n_clicks"),
     Input("info-backdrop", "n_clicks")],
    [State("info-card", "style"),
     State("info-backdrop", "style")],
    prevent_initial_call=True
)
def toggle_info_window(btn_clicks, backdrop_clicks, card_style, backdrop_style):
    # Inizializzazione difensiva: se gli stili sono None, creali vuoti
    if card_style is None: card_style = {}
    if backdrop_style is None: backdrop_style = {}

    # Identifica chi ha cliccato
    ctx_id = ctx.triggered_id

    new_card = card_style.copy()
    new_backdrop = backdrop_style.copy()

    # Controlliamo lo stato attuale: è visibile?
    # Se 'display' non esiste, assumiamo che sia 'none' (chiuso)
    is_visible = new_card.get('display', 'none') == 'block'

    if ctx_id == "open-info-btn":
        if not is_visible:
            # APRI: Imposta block su entrambi
            new_card['display'] = 'block'
            new_backdrop['display'] = 'block'
        else:
            # CHIUDI
            new_card['display'] = 'none'
            new_backdrop['display'] = 'none'

    elif ctx_id == "info-backdrop":
        # Se clicco fuori -> CHIUDI SEMPRE
        new_card['display'] = 'none'
        new_backdrop['display'] = 'none'

    return new_card, new_backdrop


if __name__ == '__main__':
    app.run_server(debug=True)