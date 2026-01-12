from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output, State
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.map import MapView
from jbi100_app.views.radar import RadarView
from jbi100_app.data import get_data

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

# 2. Stile della Finestra RADAR
RADAR_CONTAINER_STYLE = {
    "position": "fixed",
    "top": "80px",  # Allineato in altezza con il menu di sinistra
    "right": "20px",  # Margine destro
    "width": "500px",  # Larghezza aumentata (come richiesto prima)
    "height": "auto",  # Altezza automatica o fissa
    "maxHeight": "85vh",  # Non più alto dell'80% dello schermo
    "backgroundColor": "white",
    "borderRadius": "12px",
    "boxShadow": "-5px 5px 25px rgba(0,0,0,0.2)",  # Ombra verso sinistra
    "zIndex": 1000,
    "padding": "20px",
    "display": "flex",
    "flexDirection": "column",

    # --- MODIFICA ANIMAZIONE: ASSE X ---
    "transform": "translateX(130%)",  # PARTENZA: Nascosto a DESTRA (130% sposta fuori)
    "transition": "transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1)",
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
            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "5px",
                    "padding": "0 10px"
                },
                children=[
                    html.H5("Country Details", style={"margin": 0, "color": "#555"}),
                    html.Button(
                        "×",
                        id="close-radar-btn",
                        n_clicks=0,
                        style={
                            "background": "transparent",
                            "border": "none",
                            "fontSize": "24px",
                            "cursor": "pointer",
                            "color": "#888"
                        }
                    )
                ]
            ),
            html.Div(radar_view, style={"flex": "1"})
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
    Output("radar-state-store", "data"),
    [Input(map_view.html_id, "clickData"),
     Input("close-radar-btn", "n_clicks")],
    [State("radar-state-store", "data")]
)
def toggle_radar_visibility(map_click, close_click, is_open):
    trigger = ctx.triggered_id
    if not trigger: return False

    if trigger == map_view.html_id and map_click:
        return True
    if trigger == "close-radar-btn":
        return False

    return is_open

@app.callback(
    Output("radar-drawer", "style"),
    Input("radar-state-store", "data")
)
def update_radar_visuals(is_open):
    # Copiamo lo stile base
    style = RADAR_CONTAINER_STYLE.copy()

    if is_open:
        # PORTALO DENTRO (Posizione 0)
        style["transform"] = "translateX(0)"
    else:
        # BUTTALO FUORI A DESTRA
        style["transform"] = "translateX(130%)"

    return style

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


if __name__ == '__main__':
    app.run_server(debug=True)