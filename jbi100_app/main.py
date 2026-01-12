from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from .views.menu import make_menu_layout
from .views.map import MapView
from .views.radar import RadarView
from .views.compare import CompareView
from .data import get_data

app = Dash(__name__)
app.title = "Humanitarian Risk Viz"

df = get_data()

map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)
compare_view = CompareView("Compare View", df)

app.layout = html.Div(
    id="app-container",
    children=[
        make_menu_layout(),

        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                html.Div(
                    children=[map_view],
                    style={'height': '60vh', 'marginBottom': '20px'}
                ),

                # Tabs: Task 1 detail vs Task 2 comparison
                html.Div(
                    style={'height': '40vh'},
                    children=[
                        dcc.Tabs(
                            id="bottom-tabs",
                            value="tab-radar",
                            children=[
                                dcc.Tab(label="Country Detail (Task 1)", value="tab-radar", children=[radar_view]),
                                dcc.Tab(label="Compare (Task 2)", value="tab-compare", children=[compare_view]),
                            ],
                        )
                    ]
                )
            ],
        ),
    ],
)

# --- Callback A: aggiorna mappa ---
@app.callback(
    Output(map_view.html_id, "figure"),
    Input("select-risk-variable", "value")
)
def update_map(selected_risk):
    return map_view.update(selected_risk)

# --- Callback B: radar da click mappa (Task 1) ---
@app.callback(
    Output(radar_view.html_id, "figure"),
    Input(map_view.html_id, "clickData")
)
def update_radar(click_data):
    selected_country = None
    if click_data:
        selected_country = click_data['points'][0]['location']
    return radar_view.update(selected_country)

# --- Callback C: popola opzioni del dropdown paesi ---
@app.callback(
    Output("compare-countries", "options"),
    Input("compare-countries", "id")  # trigger dummy
)
def init_country_options(_):
    countries = sorted(df["Country"].dropna().unique().tolist())
    return [{"label": c, "value": c} for c in countries]

# --- Callback D: aggiungi paese da click mappa nello store ---
@app.callback(
    Output("compare-store", "data"),
    Input(map_view.html_id, "clickData"),
    State("compare-store", "data"),
    prevent_initial_call=True
)
def add_country_from_map(click_data, current_list):
    if not click_data:
        return current_list
    country = click_data["points"][0]["location"]
    if country and country not in current_list:
        return current_list + [country]
    return current_list

# --- Callback E: clear store ---
@app.callback(
    Output("compare-store", "data", allow_duplicate=True),
    Input("clear-compare", "n_clicks"),
    prevent_initial_call=True
)
def clear_compare(n):
    if n and n > 0:
        return []
    return []

# --- Callback F: sync store -> dropdown value ---
@app.callback(
    Output("compare-countries", "value"),
    Input("compare-store", "data")
)
def sync_store_to_dropdown(store_data):
    return store_data or []

# --- Callback G: sync dropdown -> store (se user modifica manualmente) ---
@app.callback(
    Output("compare-store", "data", allow_duplicate=True),
    Input("compare-countries", "value"),
    prevent_initial_call=True
)
def sync_dropdown_to_store(dropdown_value):
    return dropdown_value or []

# --- Callback H: aggiorna grafico compare (Task 2) ---
@app.callback(
    Output(compare_view.html_id, "figure"),
    Input("compare-store", "data"),
    Input("compare-dimensions", "value")
)
def update_compare(selected_countries, selected_dims):
    return compare_view.update(selected_countries, selected_dims)
