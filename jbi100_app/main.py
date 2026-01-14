from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output, State
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.map import MapView
from jbi100_app.views.radar import RadarView
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.data import get_data

app = Dash(__name__)
app.title = "Humanitarian Risk Viz"

df = get_data()
map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)

pca_scatter = Scatterplot(
    name="PCA Risk Space",
    feature_x="PC1",
    feature_y="PC2",
    df=df
)

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
    "top": "80px",
    "right": "20px",
    "width": "500px",
    "height": "auto",
    "maxHeight": "85vh",
    "backgroundColor": "white",
    "borderRadius": "16px",
    "boxShadow": "0 8px 32px rgba(0, 0, 0, 0.15)",
    "zIndex": 1000,
    "padding": "24px",
    "display": "flex",
    "flexDirection": "column",
    "transform": "translateX(130%)",
    "transition": "transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1)",
    "border": "1px solid rgba(230, 230, 235, 0.8)"
}

# 3. Bottone Hamburger
HAMBURGER_STYLE = {
    "position": "fixed",
    "top": "20px",
    "left": "20px",
    "zIndex": 2100,
    "backgroundColor": "white",
    "border": "1px solid rgba(230, 230, 235, 0.8)",
    "borderRadius": "50%",
    "width": "54px",
    "height": "54px",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "cursor": "pointer",
    "fontSize": "24px",
    "boxShadow": "0 4px 16px rgba(0,0,0,0.12)",
    "color": "#2c3e50",
    "transition": "all 0.2s ease",
    "fontWeight": "300"
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

# 5. PCA Container Style
PCA_CONTAINER_STYLE = {
    "position": "fixed",
    "bottom": "20px",
    "right": "20px",
    "width": "550px",
    "height": "520px",
    "backgroundColor": "white",
    "borderRadius": "16px",
    "boxShadow": "0 8px 32px rgba(0, 0, 0, 0.15)",
    "zIndex": 1010,
    "padding": "24px",
    "display": "flex",
    "flexDirection": "column",
    "transform": "translateY(120%)",
    "transition": "transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1)",
    "border": "1px solid rgba(230, 230, 235, 0.8)"
}


app.layout = html.Div([
    dcc.Store(id='menu-state-store', data=False),
    dcc.Store(id='radar-state-store', data=False),
    dcc.Store(id='pca-state-store', data=False),
    dcc.Store(id='brushed-countries-store', data=[]),  # Store brushed countries

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
                    "marginBottom": "16px",
                    "padding": "0 4px",
                    "borderBottom": "2px solid rgba(100, 149, 237, 0.2)",
                    "paddingBottom": "12px"
                },
                children=[
                    html.H5("Country Details", style={
                        "margin": 0,
                        "color": "#2c3e50",
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "letterSpacing": "0.3px"
                    }),
                    html.Button(
                        "×",
                        id="close-radar-btn",
                        n_clicks=0,
                        style={
                            "background": "transparent",
                            "border": "none",
                            "fontSize": "28px",
                            "cursor": "pointer",
                            "color": "#95a5a6",
                            "transition": "color 0.2s",
                            "padding": "0",
                            "width": "32px",
                            "height": "32px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "borderRadius": "50%"
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
    ),
    
    # PCA Scatterplot Drawer
    html.Div(
        id="pca-drawer",
        style=PCA_CONTAINER_STYLE,
        children=[
            # Header + Close Button
            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "16px",
                    "padding": "0 4px",
                    "borderBottom": "2px solid rgba(100, 149, 237, 0.2)",
                    "paddingBottom": "12px"
                },
                children=[
                    html.H5("PCA Risk Space", style={
                        "margin": 0,
                        "color": "#2c3e50",
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "letterSpacing": "0.3px"
                    }),
                    html.Button(
                        "×",
                        id="close-pca-btn",
                        n_clicks=0,
                        style={
                            "background": "transparent",
                            "border": "none",
                            "fontSize": "28px",
                            "cursor": "pointer",
                            "color": "#95a5a6",
                            "transition": "color 0.2s",
                            "padding": "0",
                            "width": "32px",
                            "height": "32px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "borderRadius": "50%"
                        }
                    )
                ]
            ),

            # Graph content
            html.Div(
                dcc.Graph(
                    id=pca_scatter.html_id,
                    figure=pca_scatter.update('rgb(255,100,100)', None),
                    style={"height": "100%"}
                ),
                style={"flex": "1", "overflow": "hidden"}
            )
        ]
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


# B. Radar Visibility Logic
@app.callback(
    Output("radar-state-store", "data"),
    [Input(map_view.html_id, "clickData"),
     Input("close-radar-btn", "n_clicks")],
    [State("radar-state-store", "data")]
)
def toggle_radar_visibility(map_click, close_click, is_open):
    trigger = ctx.triggered_id
    if not trigger:
        return False

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
    style = RADAR_CONTAINER_STYLE.copy()

    if is_open:
        style["transform"] = "translateX(0)"
    else:
        style["transform"] = "translateX(130%)"

    return style


# C. Store Brushed Countries from PCA
@app.callback(
    Output("brushed-countries-store", "data"),
    Input(pca_scatter.html_id, "selectedData")
)
def store_brushed_countries(selected_data):
    """Extract country names from brushed points in PCA scatter"""
    if selected_data is None or 'points' not in selected_data:
        return []
    
    # Get indices of selected points
    selected_indices = [point['pointIndex'] for point in selected_data['points']]
    
    # Get country names from dataframe using indices
    # Assumes df has a 'Country' column or similar
    brushed_countries = df.iloc[selected_indices]['Country'].tolist() if 'Country' in df.columns else []
    
    return brushed_countries


# D. Map Update with Brushed Countries
@app.callback(
    Output(map_view.html_id, "figure"),
    [Input("select-risk-variable", "value"),
     Input("brushed-countries-store", "data")]
)
def update_map(selected_risk, brushed_countries):
    """Update map with risk variable and highlight brushed countries"""
    return map_view.update(selected_risk, brushed_countries)


# E. Radar Data Update
@app.callback(
    Output(radar_view.html_id, "figure"),
    [Input(map_view.html_id, "clickData"),
     Input("select-risk-variable", "value")]
)
def update_radar_data(click_data, selected_risk):
    country = click_data['points'][0]['location'] if click_data else None
    return radar_view.update(country, selected_risk)


# F. PCA Visibility Toggle
@app.callback(
    Output("pca-state-store", "data"),
    [Input(map_view.html_id, "clickData"),
     Input("close-pca-btn", "n_clicks")],
    [State("pca-state-store", "data")]
)
def toggle_pca_visibility(map_click, close_click, is_open):
    trigger = ctx.triggered_id
    if not trigger:
        return False

    if trigger == map_view.html_id and map_click:
        return True
    if trigger == "close-pca-btn":
        return False

    return is_open


# G. PCA Drawer Animation
@app.callback(
    Output("pca-drawer", "style"),
    Input("pca-state-store", "data")
)
def update_pca_visuals(is_open):
    style = PCA_CONTAINER_STYLE.copy()

    if is_open:
        style["transform"] = "translateY(0)"
    else:
        style["transform"] = "translateY(120%)"

    return style


# H. PCA Graph Update
@app.callback(
    Output(pca_scatter.html_id, "figure"),
    [Input(map_view.html_id, "clickData"),
     Input("select-risk-variable", "value")],
)
def update_pca_graph(map_click, selected_risk):
    """Highlight clicked country in PCA scatter"""
    selected_color = "rgb(255,100,100)"
    return pca_scatter.update(selected_color, map_click)


if __name__ == '__main__':
    app.run_server(debug=True)