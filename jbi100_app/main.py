from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output, State
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.map import MapView
from jbi100_app.views.radar import RadarView
from jbi100_app.views.compare import CompareView
from jbi100_app.data import get_data
import dash

app = Dash(__name__)
app.title = "Humanitarian Risk Viz"

df = get_data()
map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)
compare_view = CompareView("Compare View", df)

all_countries = sorted(df['Country'].unique().tolist())

# --- STILI CSS ---

MENU_CONTAINER_STYLE = {
    "position": "fixed", "top": "80px", "left": "20px", "zIndex": 2000,
    "width": "fit-content", "height": "auto", "maxHeight": "85vh",
    "overflow": "visible", "opacity": 0, "visibility": "hidden",
    "transition": "opacity 0.3s ease-in-out, visibility 0.3s ease-in-out",
    "display": "block"
}

RADAR_CONTAINER_STYLE = {
    "position": "fixed", "top": "100px", "left": "100px",
    "width": "400px", "height": "auto", "maxHeight": "80vh",
    "backgroundColor": "white", "borderRadius": "12px",
    "boxShadow": "0 10px 30px rgba(0,0,0,0.3)", "zIndex": 1000,
    "padding": "20px", "display": "none", "flexDirection": "column",
    "cursor": "default"
}

HAMBURGER_STYLE = {
    "position": "fixed", "top": "20px", "left": "20px", "zIndex": 2100,
    "backgroundColor": "white", "border": "none", "borderRadius": "50%",
    "width": "50px", "height": "50px", "display": "flex",
    "alignItems": "center", "justifyContent": "center", "cursor": "pointer",
    "fontSize": "24px", "boxShadow": "0 4px 10px rgba(0,0,0,0.2)", "color": "#333"
}

BACKDROP_STYLE = {
    "position": "fixed", "top": 0, "left": 0, "width": "100vw", "height": "100vh",
    "backgroundColor": "rgba(0,0,0,0.5)", "zIndex": 1900, "display": "none",
    "backdropFilter": "blur(3px)"
}

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

# --- COMPARE MODE (tuo stile, lasciato uguale) ---
COMPARE_BTN_STYLE = {
    "position": "fixed",
    "top": "25px",
    "left": "90px",
    "zIndex": 2100,
    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "color": "white",
    "border": "none",
    "padding": "10px 25px",
    "borderRadius": "50px",
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
    "top": "80px",
    "left": "90px",
    "zIndex": 2000,
    "width": "280px",
    "backgroundColor": "white",
    "borderRadius": "12px",
    "padding": "15px",
    "boxShadow": "0 8px 30px rgba(0,0,0,0.15)",
    "display": "none",
    "border": "1px solid #eee"
}

# ✅ NUOVO: compare drawer diventa “tenda”
COMPARE_SHEET_BASE_STYLE = {
    "position": "fixed",
    "bottom": "0",
    "left": "0",
    "width": "100vw",
    "backgroundColor": "white",
    "zIndex": 1500,
    "boxShadow": "0 -5px 20px rgba(0,0,0,0.12)",
    "borderTopLeftRadius": "20px",
    "borderTopRightRadius": "20px",
    "padding": "12px 22px",
    "display": "none",
    "transition": "height 0.25s ease-in-out",
    "boxSizing": "border-box",
    "overflow": "hidden"
}

# altezze tenda
SHEET_COLLAPSED_HEIGHT = "64px"   # focus mappa
SHEET_EXPANDED_HEIGHT  = "60vh"   # focus plot (non taglia)

app.layout = html.Div([
    # Stores
    dcc.Store(id='menu-state-store', data=False),
    dcc.Store(id='radar-state-store', data=False),
    dcc.Store(id='pca-state-store', data=False),
    dcc.Store(id='brushed-countries-store', data=[]),
    dcc.Store(id='compare-mode-store', data=False),
    dcc.Store(id='selected-countries-store', data=[]),
    dcc.Store(id='explore-mode-store', data=False),  # NEW
    dcc.Store(id='compare-sheet-store', data='collapsed'),  # NEW for sheet state
    
    # Invisible overlay to capture clicks anywhere on screen
    html.Div(
        id="click-capture-overlay",
        n_clicks=0,
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "width": "100vw",
            "height": "100vh",
            "zIndex": 0,
            "pointerEvents": "auto"
        }
    ),

    dcc.Store(id='compare-mode-store', data=False),
    dcc.Store(id='selected-countries-store', data=[]),

    # ✅ nuovo store per la tenda
    dcc.Store(id='compare-sheet-store', data="collapsed"),  # collapsed | expanded

    # Menu esistente
    html.Button("☰", id="hamburger-btn", n_clicks=0, style=HAMBURGER_STYLE),
    html.Div(id="menu-backdrop", style=BACKDROP_STYLE, n_clicks=0),
    html.Div(
        id="menu-drawer",
        style=MENU_CONTAINER_STYLE,
        children=[html.Div(make_menu_layout(), style={"minWidth": "300px"})]
    ),

    # Compare UI
    html.Button("Compare Countries", id="compare-btn", n_clicks=0, style=COMPARE_BTN_STYLE),

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

    # ✅ Compare Sheet (tenda)
    html.Div(id="compare-drawer", style={**COMPARE_SHEET_BASE_STYLE, "height": SHEET_COLLAPSED_HEIGHT}, children=[
        # Header tenda + controlli focus
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"},
            children=[
                html.Div([
                    # maniglia
                    html.Div(style={
                        "width": "54px", "height": "6px",
                        "borderRadius": "999px",
                        "backgroundColor": "#ddd",
                        "margin": "0 auto 6px auto"
                    }),
                    html.Div("Comparison", style={"fontWeight": "bold", "fontSize": "14px", "color": "#333"})
                ], style={"display": "flex", "flexDirection": "column"}),

                html.Div(style={"display": "flex", "alignItems": "center"}, children=[
                    html.Button(
                        "FOCUS MAP",
                        id="focus-map-btn",
                        n_clicks=0,
                        style={
                            "border": "none", "borderRadius": "12px",
                            "padding": "8px 10px", "cursor": "pointer",
                            "backgroundColor": "#f1f1f1", "fontWeight": "bold"
                        }
                    ),
                    html.Button(
                        "FOCUS PLOT",
                        id="focus-plot-btn",
                        n_clicks=0,
                        style={
                            "border": "none", "borderRadius": "12px",
                            "padding": "8px 10px", "cursor": "pointer",
                            "backgroundColor": "#6f42c1", "color": "white",
                            "fontWeight": "bold", "marginLeft": "8px"
                        }
                    ),
                    html.Button(
                        "×",
                        id="close-compare-btn",
                        n_clicks=0,
                        style={
                            "marginLeft": "10px",
                            "border": "none", "background": "transparent",
                            "fontSize": "22px", "cursor": "pointer"
                        }
                    )
                ])
            ]
        ),

        # Body plot (non tagliato in expanded)
        html.Div(
            id="compare-body",
            style={"height": f"calc(100% - {SHEET_COLLAPSED_HEIGHT})", "paddingTop": "8px", "overflowY": "auto"},
            children=[
                html.Div(compare_view, style={"height": "100%", "width": "100%"})
            ]
        )
    ]),

    # Radar drawer esistente
    html.Div(id="radar-drawer", style=RADAR_CONTAINER_STYLE, children=[
        html.Div(id="radar-header",
                 style={"display": "flex", "justifyContent": "space-between", "alignItems": "center",
                        "marginBottom": "15px", "padding": "10px", "cursor": "move",
                        "backgroundColor": "#f9f9f9", "borderBottom": "1px solid #eee",
                        "borderRadius": "12px 12px 0 0"},
                 children=[
                     html.H5("Country Details", style={"margin": 0, "userSelect": "none"}),
                     html.Button("×", id="close-radar-btn", n_clicks=0,
                                 style={"border": "none", "background": "transparent", "fontSize": "20px",
                                        "cursor": "pointer"})
                 ]),
        html.Div(radar_view, style={"flex": "1", "padding": "0 10px"})
    ]),

    # Zoom
    html.Div(style=ZOOM_CONTAINER_STYLE, children=[
        html.Button("+", id="btn-zoom-in", n_clicks=0, style=ZOOM_BTN_STYLE),
        html.Button("-", id="btn-zoom-out", n_clicks=0, style={**ZOOM_BTN_STYLE, "borderBottom": "none"})
    ]),

    # Mappa fullscreen
    html.Div(
        style={"height": "100vh", "width": "100vw", "position": "absolute", "top": 0, "left": 0, "zIndex": 1},
        children=[map_view]
    )
])


# ---------------- MENU LOGIC (come tuo) ----------------

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


# ---------------- COMPARE MODE ----------------

@app.callback(
    [Output("compare-mode-store", "data"),
     Output("compare-search-panel", "style"),
     Output("compare-drawer", "style"),
     Output("compare-btn", "style"),
     Output("compare-btn", "children"),
     Output("selected-countries-store", "data"),
     Output("compare-sheet-store", "data")],
    [Input("compare-btn", "n_clicks"),
     Input("close-compare-btn", "n_clicks"),
     Input("focus-map-btn", "n_clicks"),
     Input("focus-plot-btn", "n_clicks")],
    [State("compare-mode-store", "data"),
     State("compare-sheet-store", "data")]
)
def compare_controller(n_compare, n_close, n_focus_map, n_focus_plot, is_active, sheet_state):
    trigger = ctx.triggered_id
    if not trigger:
        return (dash.no_update,) * 7

    search_style = COMPARE_PANEL_STYLE.copy()
    drawer_style = COMPARE_SHEET_BASE_STYLE.copy()
    btn_style = COMPARE_BTN_STYLE.copy()

    # default: lascia sheet_state com'è
    new_sheet_state = sheet_state or "collapsed"

    # ---- CHIUSURA compare ----
    if trigger == "close-compare-btn":
        search_style["display"] = "none"
        drawer_style["display"] = "none"
        drawer_style["height"] = SHEET_COLLAPSED_HEIGHT
        btn_style["background"] = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        return False, search_style, drawer_style, btn_style, "Compare Countries", [], "collapsed"

    # ---- TOGGLE compare ----
    if trigger == "compare-btn":
        new_state = not is_active

        if new_state:
            # apertura: mostra panel + sheet (collassata)
            search_style["display"] = "block"
            drawer_style["display"] = "block"
            drawer_style["height"] = SHEET_COLLAPSED_HEIGHT
            btn_style["background"] = "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)"
            return True, search_style, drawer_style, btn_style, "Stop Comparing", dash.no_update, "collapsed"
        else:
            # chiusura: nascondi tutto e reset selezione
            search_style["display"] = "none"
            drawer_style["display"] = "none"
            drawer_style["height"] = SHEET_COLLAPSED_HEIGHT
            btn_style["background"] = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
            return False, search_style, drawer_style, btn_style, "Compare Countries", [], "collapsed"

    # ---- FOCUS (solo se compare è attivo) ----
    if not is_active:
        return (dash.no_update,) * 7

    if trigger == "focus-plot-btn":
        new_sheet_state = "expanded"
    elif trigger == "focus-map-btn":
        new_sheet_state = "collapsed"

    # applichiamo lo stato sheet al drawer
    drawer_style["display"] = "block"
    drawer_style["height"] = SHEET_EXPANDED_HEIGHT if new_sheet_state == "expanded" else SHEET_COLLAPSED_HEIGHT

    # quando focus, non tocchiamo compare-mode / btn / selezione
    # ma dobbiamo restituire i valori correnti (no_update non va bene perché stiamo già ritornando stili)
    search_style["display"] = "block"
    btn_style["background"] = "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)"

    return True, search_style, drawer_style, btn_style, "Stop Comparing", dash.no_update, new_sheet_state


@app.callback(
    Output("compare-drawer", "style", allow_duplicate=True),
    [Input("compare-sheet-store", "data"),
     Input("compare-mode-store", "data")],
    State("compare-drawer", "style"),
    prevent_initial_call=True
)
def apply_compare_sheet_style(sheet_state, compare_on, current_style):
    if current_style is None:
        current_style = COMPARE_SHEET_BASE_STYLE.copy()

    new_style = current_style.copy()

    # se compare off, non toccare (lo gestisce toggle_compare_mode)
    if not compare_on:
        return new_style

    new_style["display"] = "block"
    new_style["height"] = SHEET_EXPANDED_HEIGHT if sheet_state == "expanded" else SHEET_COLLAPSED_HEIGHT
    return new_style


# B2. Gestione Selezione (Mappa + Dropdown) — COME TUO, ma robusto
@app.callback(
    Output("country-selector", "value"),
    [Input(map_view.html_id, "clickData"),
     Input("country-selector", "value")],
    [State("compare-mode-store", "data")]
)
def manage_selection_ui(map_click, dropdown_value, compare_mode):
    trigger = ctx.triggered_id

    # click su mappa quando compare OFF => ignoralo
    if (not compare_mode) and trigger == map_view.html_id:
        return dash.no_update

    # dropdown = fonte di verità
    if trigger == "country-selector":
        return dropdown_value

    # mappa = toggle
    if trigger == map_view.html_id and map_click:
        clicked_country = map_click['points'][0]['location']
        current_list = dropdown_value or []
        if clicked_country in current_list:
            return [c for c in current_list if c != clicked_country]
        return current_list + [clicked_country]

    return dash.no_update


@app.callback(
    Output("selected-countries-store", "data", allow_duplicate=True),
    Input("country-selector", "value"),
    prevent_initial_call=True
)
def sync_store(value):
    return value or []


@app.callback(
    Output(compare_view.html_id, "figure"),
    Input("selected-countries-store", "data")
)
def update_compare_view(selected_countries):
    return compare_view.update(selected_countries)


# ---------------- RADAR VISIBILITY (come tuo, ma NON resetta clickData) ----------------

@app.callback(
    [Output("radar-state-store", "data"),
     Output(map_view.html_id, "clickData")],
    [Input(map_view.html_id, "clickData"),
     Input("close-radar-btn", "n_clicks")],
    [State("radar-state-store", "data"),
     State("compare-mode-store", "data")]
)
def toggle_radar_visibility(map_click, close_click, is_open, is_compare_mode):
    trigger = ctx.triggered_id
    if not trigger:
        return is_open, dash.no_update

    # Se compare mode attiva: radar chiuso, MA non resettare clickData
    if is_compare_mode:
        return False, dash.no_update

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
    if current_style is None:
        current_style = RADAR_CONTAINER_STYLE.copy()
    new_style = current_style.copy()
    if is_open:
        new_style["display"] = "flex"
        new_style["transform"] = "none"
    else:
        new_style["display"] = "none"
    return new_style


# ---------------- MAPPA / RADAR DATA ----------------

@app.callback(
    Output(map_view.html_id, "figure"),
    [Input("select-risk-variable", "value"),
     Input("selected-countries-store", "data")]
)
def update_map(selected_risk, selected_countries):
    return map_view.update(selected_risk, selected_countries)


@app.callback(
    Output(radar_view.html_id, "figure"),
    [Input(map_view.html_id, "clickData"),
     Input("select-risk-variable", "value")]
)
def update_radar_data(click_data, selected_risk):
    country = click_data['points'][0]['location'] if click_data else None
    return radar_view.update(country, selected_risk)


# ---------------- INFO WINDOW (come tuo) ----------------

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