from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output, State
from jbi100_app.data import get_data
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.map_view import MapView
from jbi100_app.views.radar import RadarView
import dash
import plotly.graph_objects as go

app = Dash(__name__)
app.title = "Humanitarian Risk Viz"

df = get_data()
map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)

# --- STILI CSS ---

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

RADAR_CONTAINER_STYLE = {
    "position": "fixed",
    "top": "100px",
    "left": "100px",
    "width": "400px",
    "height": "auto",
    "maxHeight": "80vh",
    "backgroundColor": "white",
    "borderRadius": "12px",
    "boxShadow": "0 10px 30px rgba(0,0,0,0.3)",
    "zIndex": 1000,
    "padding": "20px",
    "display": "none",
    "flexDirection": "column",
    "cursor": "default"
}

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
    dcc.Store(id='compare-mode-store', data=False),
    dcc.Store(id='compare-countries-store', data=[]),

    html.Button("☰", id="hamburger-btn", n_clicks=0, style=HAMBURGER_STYLE),
    html.Div(id="menu-backdrop", style=BACKDROP_STYLE, n_clicks=0),

    html.Div(
        id="menu-drawer",
        style=MENU_CONTAINER_STYLE,
        children=[
            html.Div(children=[make_menu_layout(include_compare=True)], style={"minWidth": "300px"})
        ]
    ),

    html.Div(
        id="radar-drawer",
        style=RADAR_CONTAINER_STYLE,
        children=[
            html.Div(
                id="radar-header",
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "15px",
                    "padding": "10px",
                    "cursor": "move",
                    "backgroundColor": "#f9f9f9",
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
            html.Div(radar_view, style={"flex": "1", "padding": "0 10px"})
        ]
    ),

    html.Div(
        style=ZOOM_CONTAINER_STYLE,
        children=[
            html.Button("+", id="btn-zoom-in", n_clicks=0, style=ZOOM_BTN_STYLE),
            html.Button("-", id="btn-zoom-out", n_clicks=0, style={**ZOOM_BTN_STYLE, "borderBottom": "none"})
        ]
    ),

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
    if not trigger:
        return False

    if trigger == "select-risk-variable":
        return False
    if trigger == "hamburger-btn":
        return not is_open
    if trigger == "menu-backdrop":
        return False

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


# B. Compare mode toggle
@app.callback(
    [Output("compare-mode-store", "data"),
     Output("toggle-compare-btn", "children"),
     Output("compare-controls", "style")],
    Input("toggle-compare-btn", "n_clicks"),
    State("compare-mode-store", "data"),
    prevent_initial_call=True
)
def toggle_compare_mode(n, is_on):
    new_on = not is_on
    label = "Deactivate Compare Mode" if new_on else "Activate Compare Mode"
    controls_style = {"display": "block"} if new_on else {"display": "none"}
    return new_on, label, controls_style


# C. Popola dropdown paesi
@app.callback(
    Output("compare-dropdown", "options"),
    Input("menu-state-store", "data")
)
def fill_compare_options(_):
    return [{"label": c, "value": c} for c in sorted(df["Country"].unique())]


# D. Selezione paesi da LISTA + CLEAR
@app.callback(
    Output("compare-countries-store", "data"),
    [Input("compare-dropdown", "value"),
     Input("clear-compare-btn", "n_clicks")],
    State("compare-countries-store", "data"),
    prevent_initial_call=True
)
def update_compare_countries_from_list(dropdown_values, n_clear, current):
    trig = ctx.triggered_id
    if trig == "clear-compare-btn":
        return []
    return dropdown_values or []


# E. Selezione paesi da MAPPA
@app.callback(
    Output("compare-countries-store", "data", allow_duplicate=True),
    Input(map_view.html_id, "clickData"),
    [State("compare-mode-store", "data"),
     State("compare-countries-store", "data")],
    prevent_initial_call=True
)
def toggle_country_from_map(click_data, compare_on, selected):
    if not compare_on:
        return dash.no_update

    if not click_data:
        return dash.no_update

    country = click_data["points"][0]["location"]
    selected = selected or []

    if country in selected:
        selected = [c for c in selected if c != country]
    else:
        selected = selected + [country]

    return selected


# F. Mantieni dropdown sincronizzato
@app.callback(
    Output("compare-dropdown", "value"),
    Input("compare-countries-store", "data")
)
def sync_dropdown(selected):
    return selected or []


# G. Radar Visibility Logic
@app.callback(
    [Output("radar-state-store", "data"),
     Output(map_view.html_id, "clickData")],
    [Input(map_view.html_id, "clickData"),
     Input("close-radar-btn", "n_clicks")],
    [State("radar-state-store", "data"),
     State("compare-mode-store", "data")]
)
def toggle_radar_visibility(map_click, close_click, is_open, compare_on):
    trigger = ctx.triggered_id

    if not trigger:
        return is_open, dash.no_update

    if trigger == "close-radar-btn":
        return False, None

    if compare_on:
        return False, dash.no_update

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


# H. AGGIORNAMENTO MAPPA con paesi selezionati
@app.callback(
    Output(map_view.html_id, "figure"),
    [Input("select-risk-variable", "value"),
     Input("compare-countries-store", "data")]
)
def update_map(selected_risk, compare_countries):
    return map_view.update(selected_risk, compare_countries or [])


# I. RADAR DATA
@app.callback(
    Output(radar_view.html_id, "figure"),
    [Input(map_view.html_id, "clickData"),
     Input("select-risk-variable", "value")]
)
def update_radar_data(click_data, selected_risk):
    country = click_data['points'][0]['location'] if click_data else None
    return radar_view.update(country, selected_risk)


# J. Parallel Plot
@app.callback(
    [Output("parallel-container", "style"),
     Output("parallel-plot", "figure")],
    Input("open-parallel-btn", "n_clicks"),
    [State("compare-countries-store", "data"),
     State("parallel-container", "style")],
    prevent_initial_call=True
)
def show_parallel(n, countries, current_style):
    countries = countries or []

    if not countries:
        return {"display": "none"}, go.Figure()

    dims = ["Economic Risk", "Social Risk", "Infrastructure Risk", "Demographic Risk"]
    df_sel = df[df["Country"].isin(countries)].copy()
    if df_sel.empty:
        return {"display": "none"}, go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Parcoords(
        line=dict(color=list(range(len(df_sel))), showscale=False),
        dimensions=[dict(label=c, values=df_sel[c].astype(float), range=[0, 1]) for c in dims],
        customdata=df_sel["Country"].tolist(),
        hoveron="lines",
        hovertemplate="Country: %{customdata}<extra></extra>",
    ))

    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        title=dict(text="Parallel Plot", x=0.5, font=dict(size=14)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return {"display": "block"}, fig


# K. INFO WINDOW
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
    if card_style is None:
        card_style = {}
    if backdrop_style is None:
        backdrop_style = {}

    ctx_id = ctx.triggered_id

    new_card = card_style.copy()
    new_backdrop = backdrop_style.copy()

    is_visible = new_card.get('display', 'none') == 'block'

    if ctx_id == "open-info-btn":
        if not is_visible:
            new_card['display'] = 'block'
            new_backdrop['display'] = 'block'
        else:
            new_card['display'] = 'none'
            new_backdrop['display'] = 'none'

    elif ctx_id == "info-backdrop":
        new_card['display'] = 'none'
        new_backdrop['display'] = 'none'

    return new_card, new_backdrop


if __name__ == '__main__':
    app.run_server(debug=True)
