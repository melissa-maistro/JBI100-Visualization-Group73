from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output, State
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.map import MapView
from jbi100_app.views.radar import RadarView
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.compare import CompareView
from jbi100_app.views.transport_rank import TransportRankView
from jbi100_app.data import get_data
import dash
from jbi100_app.views.explore_panel import ExplorePanel
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.graph_objects as go
from sklearn.impute import SimpleImputer

# test

app = Dash(__name__)
app.title = "Humanitarian Risk Viz"

df = get_data()
map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)
compare_view = CompareView("Compare View", df)
transport_rank_view = TransportRankView("Transport Rank", df)
explore_panel = ExplorePanel("Explore Panel")



# Lista paesi per il dropdown
all_countries = sorted(df['Country'].unique().tolist())
transport_slider_max = 25
transport_slider_marks = {5: "5", 10: "10", 15: "15", 20: "20", 25: "25"}

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

# 5. PCA Container Style (Now used for the drawer)
PCA_CONTAINER_STYLE = {
    "position": "fixed",
    "bottom": "0",
    "left": "0",
    "width": "100vw",
    "height": "60vh",
    "backgroundColor": "white",
    "zIndex": 1500,
    "boxShadow": "0 -5px 20px rgba(0,0,0,0.1)",
    "borderTopLeftRadius": "20px",
    "borderTopRightRadius": "20px",
    "padding": "20px 30px",
    "display": "none",
    "transition": "transform 0.3s ease-in-out",
    "boxSizing": "border-box"
}

# 6. Compare Button Style
COMPARE_BTN_STYLE = {
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
    "textTransform": "uppercase",
    "whiteSpace": "nowrap"
}

# 7. Compare Panel Style
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

# 8. Compare Drawer Style (Base style, height will be dynamic)
COMPARE_SHEET_BASE_STYLE = {
    "position": "fixed",
    "bottom": "0",
    "left": "0",
    "width": "100vw",
    "height": "65vh",  # default, will be overridden
    "backgroundColor": "white",
    "zIndex": 1500,
    "boxShadow": "0 -5px 20px rgba(0,0,0,0.1)",
    "borderTopLeftRadius": "20px",
    "borderTopRightRadius": "20px",
    "padding": "20px 30px",
    "display": "none",
    "transition": "height 0.3s ease-in-out",
    "boxSizing": "border-box"
}

SHEET_COLLAPSED_HEIGHT = "250px"
SHEET_EXPANDED_HEIGHT = "65vh"

# Keep old style name for backwards compatibility
COMPARE_DRAWER_STYLE = COMPARE_SHEET_BASE_STYLE

# 9. Explore Button Style (NEW)
EXPLORE_BTN_STYLE = {
    "background": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
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
    "textTransform": "uppercase",
    "whiteSpace": "nowrap"
}

# 10. Transport Button Style (NEW)
TRANSPORT_BTN_STYLE = {
    "background": "linear-gradient(135deg, #f7971e 0%, #ffd200 100%)",
    "color": "#2c3e50",
    "border": "none",
    "padding": "10px 22px",
    "borderRadius": "50px",
    "cursor": "pointer",
    "boxShadow": "0 4px 15px rgba(0,0,0,0.2)",
    "fontWeight": "bold",
    "fontSize": "13px",
    "letterSpacing": "0.4px",
    "transition": "transform 0.2s, box-shadow 0.2s",
    "textTransform": "uppercase",
    "whiteSpace": "nowrap"
}

# 10.5 Top Button Row Style (NEW)
TOP_BUTTON_ROW_STYLE = {
    "position": "fixed",
    "top": "25px",
    "left": "90px",
    "zIndex": 2100,
    "display": "flex",
    "gap": "14px",
    "alignItems": "center"
}

# 11. Transport Drawer Style (NEW)
TRANSPORT_DRAWER_STYLE = {
    "position": "fixed",
    "top": "90px",
    "right": "20px",
    "width": "360px",
    "height": "60vh",
    "backgroundColor": "white",
    "borderRadius": "16px",
    "boxShadow": "0 8px 32px rgba(0, 0, 0, 0.15)",
    "zIndex": 1800,
    "padding": "18px 20px",
    "display": "none",
    "border": "1px solid rgba(230, 230, 235, 0.8)"
}


app.layout = html.Div([
    # Stores
    dcc.Store(id='menu-state-store', data=False),
    dcc.Store(id='radar-state-store', data=False),
    dcc.Store(id='brushed-countries-store', data=[]),
    dcc.Store(id='compare-mode-store', data=False),
    dcc.Store(id='selected-countries-store', data=[]),
    dcc.Store(id='explore-mode-store', data=False),  # NEW
    dcc.Store(id='compare-sheet-store', data='collapsed'),  # NEW for sheet state
    dcc.Store(id='transport-mode-store', data=False),  # NEW
    dcc.Store(id='transport-selected-store', data=[]),  # NEW
    dcc.Store(id='explore-highlight-store', data=[]),      # lista paesi highlight da explore
    dcc.Store(id='sim-selected-store', data=[]),          # lista [anchor + topK] per "send to compare"
    dcc.Store(id='cluster-assign-store', data={}),        # dict country->cluster
    dcc.Store(id='cluster-selected-store', data=[]),       # lista paesi cluster selezionato
    
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

    # UI Elements
    html.Button("☰", id="hamburger-btn", n_clicks=0, style=HAMBURGER_STYLE),
    html.Div(id="menu-backdrop", style=BACKDROP_STYLE, n_clicks=0),

    # Top Action Buttons
    html.Div(
        id="top-action-buttons",
        style=TOP_BUTTON_ROW_STYLE,
        children=[
            html.Button("Compare Countries", id="compare-btn", n_clicks=0, style=COMPARE_BTN_STYLE),
            html.Button("Explore Correlations", id="explore-btn", n_clicks=0, style=EXPLORE_BTN_STYLE),
            html.Button("Transport Focus", id="transport-btn", n_clicks=0, style=TRANSPORT_BTN_STYLE),
        ]
    ),

    # Compare Search Panel
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

    # Compare Drawer
    html.Div(id="compare-drawer", style=COMPARE_DRAWER_STYLE, children=[
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "marginBottom": "16px",
                "padding": "0 4px",
                "borderBottom": "2px solid rgba(102, 126, 234, 0.2)",
                "paddingBottom": "12px"
            },
            children=[
                html.H5("Risk Comparison", style={
                    "margin": 0,
                    "color": "#2c3e50",
                    "fontWeight": "600",
                    "fontSize": "18px",
                    "letterSpacing": "0.3px"
                }),
                html.Div(
                    style={"display": "flex", "gap": "10px", "alignItems": "center"},
                    children=[
                        html.Button(
                            "Focus Map",
                            id="focus-map-btn",
                            n_clicks=0,
                            style={
                                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                "color": "white",
                                "border": "none",
                                "padding": "6px 16px",
                                "borderRadius": "20px",
                                "cursor": "pointer",
                                "fontSize": "12px",
                                "fontWeight": "600"
                            }
                        ),
                        html.Button(
                            "Focus Plot",
                            id="focus-plot-btn",
                            n_clicks=0,
                            style={
                                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                "color": "white",
                                "border": "none",
                                "padding": "6px 16px",
                                "borderRadius": "20px",
                                "cursor": "pointer",
                                "fontSize": "12px",
                                "fontWeight": "600"
                            }
                        ),
                        html.Button(
                            "×",
                            id="close-compare-btn",
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
                )
            ]
        ),
        html.Div(compare_view, style={"height": "calc(100% - 60px)", "width": "100%"})
    ]),



    # Transport Drawer (NEW)
    html.Div(id="transport-drawer", style=TRANSPORT_DRAWER_STYLE, children=[
        html.Div(
            style={
                "display": "flex",
                "alignItems": "center",
                "marginBottom": "12px",
                "padding": "0 4px",
                "borderBottom": "2px solid rgba(247, 151, 30, 0.25)",
                "paddingBottom": "10px"
            },
            children=[
                html.H5("Transport Intervention Finder", style={
                    "margin": 0,
                    "color": "#2c3e50",
                    "fontWeight": "600",
                    "fontSize": "16px",
                    "letterSpacing": "0.3px"
                })
            ]
        ),
        html.Div(
            className="js-no-drag",
            children=[
                html.Label("Show top N constrained countries:", style={"fontSize": "12px", "color": "#555"}),
                dcc.Slider(
                    id="transport-topn-slider",
                    min=5,
                    max=transport_slider_max,
                    step=5,
                    value=15,
                    marks=transport_slider_marks,
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
            ],
            style={"marginBottom": "10px"}
        ),
        html.Div(
            className="js-no-drag",
            children=[
                dcc.Graph(
                    id=transport_rank_view.html_id,
                    figure=transport_rank_view.update(15, []),
                    config={"displayModeBar": False},
                    style={"height": "100%"}
                )
            ],
            style={"flex": "1", "overflow": "hidden"}
        )
    ]),

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
                id ="radar-header",
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "16px",
                    "cursor": "move",
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


# B. Compare Mode Logic (Updated with sheet state and focus buttons)
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
     State("compare-sheet-store", "data"),
     State("explore-mode-store", "data")]
)
def compare_controller(n_compare, n_close, n_focus_map, n_focus_plot, is_active, sheet_state, explore_mode):
    trigger = ctx.triggered_id
    if not trigger:
        return (dash.no_update,) * 7
    
    search_style = COMPARE_PANEL_STYLE.copy()
    drawer_style = COMPARE_SHEET_BASE_STYLE.copy()
    btn_style = COMPARE_BTN_STYLE.copy()
    
    # default: leave sheet_state as is
    new_sheet_state = sheet_state or "collapsed"

    # ---- CLOSE compare ----
    if trigger == "close-compare-btn":
        search_style["display"] = "none"
        drawer_style["display"] = "none"
        drawer_style["height"] = SHEET_COLLAPSED_HEIGHT
        btn_style["background"] = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        return False, search_style, drawer_style, btn_style, "Compare Countries", [], "collapsed"
    
    # ---- TOGGLE compare ----
    if trigger == "compare-btn":
        if explore_mode and not is_active:
            return (dash.no_update,) * 7
        new_state = not is_active
        if new_state:
            # opening: show panel + sheet (collapsed)
            search_style["display"] = "block"
            drawer_style["display"] = "block"
            drawer_style["height"] = SHEET_COLLAPSED_HEIGHT
            btn_style["background"] = "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)"
            return True, search_style, drawer_style, btn_style, "Stop Comparing", dash.no_update, "collapsed"
        else:
            # closing: hide everything and reset selection
            search_style["display"] = "none"
            drawer_style["display"] = "none"
            drawer_style["height"] = SHEET_COLLAPSED_HEIGHT
            btn_style["background"] = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
            return False, search_style, drawer_style, btn_style, "Compare Countries", [], "collapsed"
    
    # ---- FOCUS (only if compare is active) ----
    if not is_active:
        return (dash.no_update,) * 7
    
    if trigger == "focus-plot-btn":
        new_sheet_state = "expanded"
    elif trigger == "focus-map-btn":
        new_sheet_state = "collapsed"
    
    # apply sheet state to drawer
    drawer_style["display"] = "block"
    drawer_style["height"] = SHEET_EXPANDED_HEIGHT if new_sheet_state == "expanded" else SHEET_COLLAPSED_HEIGHT
    
    # when focusing, don't touch compare-mode / btn / selection
    search_style["display"] = "block"
    btn_style["background"] = "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)"
    return True, search_style, drawer_style, btn_style, "Stop Comparing", dash.no_update, new_sheet_state


# B2. Explore Mode Logic (NEW)
@app.callback(
    [Output("explore-mode-store", "data"),
     Output("explore-drawer", "style"),
     Output("explore-btn", "style"),
     Output("explore-btn", "children")],
    [Input("explore-btn", "n_clicks"),
     Input("close-explore-btn", "n_clicks")],
    [State("explore-mode-store", "data"),
     State("compare-mode-store", "data")]
)
def toggle_explore_mode(btn_click, close_click, is_active, compare_mode):
    trigger = ctx.triggered_id
    if not trigger:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    new_state = not is_active if trigger == "explore-btn" else False
    
    drawer_style = PCA_CONTAINER_STYLE.copy()
    btn_style = EXPLORE_BTN_STYLE.copy()

    if new_state:
        if compare_mode:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update
        drawer_style["display"] = "flex"
        drawer_style["flexDirection"] = "column"
        btn_style["background"] = "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)"
        return True, drawer_style, btn_style, "Close Explorer"
    else:
        drawer_style["display"] = "none"
        return False, drawer_style, EXPLORE_BTN_STYLE, "Explore Correlations"

RISK_DIMS_DEFAULT = ["Economic Risk", "Social Risk", "Infrastructure Risk", "Demographic Risk"]

@app.callback(
    [Output("sim-table", "data"),
     Output("sim-delta-bar", "figure"),
     Output("explore-highlight-store", "data", allow_duplicate=True),
     Output("sim-selected-store", "data")],
    [Input("sim-anchor-country", "value"),
     Input("sim-topk", "value"),
     Input("sim-dims", "value"),
     Input("explore-mode-store", "data")],
    prevent_initial_call=True
)
def update_similarity(anchor, topk, dims, explore_on):
    if not explore_on or not anchor:
        fig = go.Figure()
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), title="Select an anchor country")
        return [], fig, [], []

    dims = dims or RISK_DIMS_DEFAULT
    dims = [d for d in dims if d in df.columns]
    if len(dims) < 2:
        fig = go.Figure()
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), title="Select at least 2 dimensions")
        return [], fig, [anchor], [anchor]

    X = df[dims].astype(float).values
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    # anchor row
    try:
        a_idx = df.index[df["Country"] == anchor][0]
    except Exception:
        fig = go.Figure()
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), title="Anchor not found")
        return [], fig, [], []

    a_vec = Xs[a_idx]
    dists = np.linalg.norm(Xs - a_vec, axis=1)

    # sort excluding anchor
    order = np.argsort(dists)
    order = [i for i in order if i != a_idx]
    topk = int(topk or 7)
    topk_idx = order[:topk]

    top_countries = df.iloc[topk_idx]["Country"].tolist()
    table_data = [{"Country": c, "Distance": float(f"{dists[df.index[df['Country']==c][0]]:.3f}")} for c in top_countries]

    # Explanation bar: mean(topK) - anchor (in original scale 0..1)
    anchor_vals = df.loc[df["Country"] == anchor, dims].iloc[0].astype(float).values
    mean_vals = df.iloc[topk_idx][dims].astype(float).mean().values
    delta = mean_vals - anchor_vals

    fig = go.Figure()
    fig.add_trace(go.Bar(x=dims, y=delta))
    fig.update_layout(
        title="How similar countries differ from the anchor (mean(topK) − anchor)",
        margin=dict(l=20, r=20, t=40, b=40),
        yaxis_title="Δ risk (positive = higher than anchor)"
    )

    highlight = [anchor] + top_countries
    sim_selected = [anchor] + top_countries

    return table_data, fig, highlight, sim_selected

@app.callback(
    Output("selected-countries-store", "data", allow_duplicate=True),
    Input("sim-send-to-compare", "n_clicks"),
    State("sim-selected-store", "data"),
    prevent_initial_call=True
)
def send_similarity_to_compare(n, sim_selected):
    if not n:
        return dash.no_update
    sim_selected = sim_selected or []
    # limitiamo per evitare spaghetti nel plot
    return sim_selected[:8]



@app.callback(
    [Output("clust-table", "data"),
     Output("clust-select", "options"),
     Output("cluster-assign-store", "data")],
    [Input("clust-k", "value"),
     Input("clust-dims", "value"),
     Input("explore-mode-store", "data")],
    prevent_initial_call=True
)
def compute_clusters(k, dims, explore_on):
    if not explore_on:
        return dash.no_update, dash.no_update, dash.no_update

    k = int(k or 4)
    dims = dims or RISK_DIMS_DEFAULT
    dims = [d for d in dims if d in df.columns]
    if len(dims) < 2:
        return [], [], {}

    X = df[dims].astype(float).values
    Xs = StandardScaler().fit_transform(X)

    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(Xs)

    # assignment dict
    assign = {df.iloc[i]["Country"]: int(labels[i]) for i in range(len(df))}

    # sizes
    sizes = pd.Series(labels).value_counts().sort_index()
    table = [{"Cluster": f"Cluster {int(cid)}", "Size": int(sizes.loc[cid])} for cid in sizes.index]

    opts = [{"label": f"Cluster {int(cid)} (n={int(sizes.loc[cid])})", "value": int(cid)} for cid in sizes.index]
    return table, opts, assign


@app.callback(
    [Output("clust-countries", "data"),
     Output("clust-explain-bar", "figure"),
     Output("explore-highlight-store", "data", allow_duplicate=True),
     Output("cluster-selected-store", "data")],
    [Input("clust-select", "value"),
     Input("cluster-assign-store", "data"),
     Input("clust-dims", "value"),
     Input("explore-mode-store", "data")],
    prevent_initial_call=True
)
def select_cluster(cluster_id, assign, dims, explore_on):
    dims = dims or RISK_DIMS_DEFAULT
    dims = [d for d in dims if d in df.columns]

    if not explore_on or cluster_id is None or not assign or len(dims) < 2:
        fig = go.Figure()
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), title="Select a cluster")
        return [], fig, [], []

    cluster_id = int(cluster_id)

    countries = [c for c, cid in assign.items() if int(cid) == cluster_id]
    countries_sorted = sorted(countries)

    # countries table
    countries_table = [{"Country": c} for c in countries_sorted]

    # explain: mean(cluster) - mean(global)
    global_mean = df[dims].astype(float).mean()
    cluster_mean = df[df["Country"].isin(countries)][dims].astype(float).mean()
    delta = (cluster_mean - global_mean).values

    fig = go.Figure()
    fig.add_trace(go.Bar(x=dims, y=delta))
    fig.update_layout(
        title="Cluster signature (mean(cluster) − mean(global))",
        margin=dict(l=20, r=20, t=40, b=40),
        yaxis_title="Δ risk (positive = higher than global mean)"
    )

    highlight = countries_sorted
    return countries_table, fig, highlight, countries_sorted


@app.callback(
    Output("selected-countries-store", "data", allow_duplicate=True),
    Input("clust-send-to-compare", "n_clicks"),
    State("cluster-selected-store", "data"),
    prevent_initial_call=True
)
def send_cluster_to_compare(n, cluster_countries):
    if not n:
        return dash.no_update
    cluster_countries = cluster_countries or []
    return cluster_countries[:8]

@app.callback(
    [Output("explore-highlight-store", "data"),
     Output("sim-anchor-country", "value"),
     Output("clust-select", "value")],
    Input("explore-mode-store", "data"),
    prevent_initial_call=True
)
def reset_explore_state(explore_on):
    if not explore_on:
        return [], None, None
    return dash.no_update, dash.no_update, dash.no_update

# B3. Transport Mode Logic (NEW)
@app.callback(
    [Output("transport-mode-store", "data"),
     Output("transport-drawer", "style"),
     Output("transport-btn", "style"),
     Output("transport-btn", "children")],
    [Input("transport-btn", "n_clicks")],
    [State("transport-mode-store", "data")]
)


def toggle_transport_mode(btn_click, is_active):
    trigger = ctx.triggered_id
    if not trigger:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    new_state = not is_active if trigger == "transport-btn" else False
    drawer_style = TRANSPORT_DRAWER_STYLE.copy()
    btn_style = TRANSPORT_BTN_STYLE.copy()

    if new_state:
        drawer_style["display"] = "flex"
        drawer_style["flexDirection"] = "column"
        btn_style["background"] = "linear-gradient(135deg, #e74c3c 0%, #f1c40f 100%)"
        return True, drawer_style, btn_style, "Close Transport"
    else:
        drawer_style["display"] = "none"
        return False, drawer_style, TRANSPORT_BTN_STYLE, "Transport Focus"


# B4. Transport Rank Update (NEW)
@app.callback(
    Output(transport_rank_view.html_id, "figure"),
    [Input("transport-topn-slider", "value"),
     Input("transport-selected-store", "data")]
)
def update_transport_rank(top_n, selected_countries):
    return transport_rank_view.update(top_n=top_n, selected_countries=selected_countries)


# B5. Transport Selection (NEW)
@app.callback(
    Output("transport-selected-store", "data"),
    [Input(transport_rank_view.html_id, "clickData"),
     Input("transport-mode-store", "data")],
    [State("transport-selected-store", "data")]
)
def update_transport_selection(click_data, transport_mode, selected_countries):
    trigger = ctx.triggered_id

    if trigger == "transport-mode-store" and not transport_mode:
        return []

    if trigger == transport_rank_view.html_id and click_data and transport_mode:
        country = click_data["points"][0].get("y")
        selected_countries = selected_countries or []
        if country in selected_countries:
            return [c for c in selected_countries if c != country]
        return selected_countries + [country]

    return dash.no_update


# C. Manage Country Selection (Dropdown + Map)
@app.callback(
    Output("country-selector", "value"),
    [Input(map_view.html_id, "clickData"),
     Input("country-selector", "value"),
     Input("compare-mode-store", "data")]
)
def manage_selection_ui(map_click, dropdown_value, compare_mode):
    trigger = ctx.triggered_id

    if trigger == "compare-mode-store" and not compare_mode:
        return []

    if not compare_mode and trigger == map_view.html_id:
        return dash.no_update

    if trigger == "country-selector":
        return dropdown_value

    if trigger == map_view.html_id and map_click:
        clicked_country = map_click['points'][0]['location']
        current_list = dropdown_value or []
        
        if clicked_country in current_list:
            new_list = [c for c in current_list if c != clicked_country]
        else:
            new_list = current_list + [clicked_country]
        
        return new_list

    return dash.no_update


# D. Sync Dropdown to Store
@app.callback(
    Output("selected-countries-store", "data", allow_duplicate=True),
    Input("country-selector", "value"),
    prevent_initial_call=True
)
def sync_store(value):
    return value or []


# E. Update Compare View
@app.callback(
    Output(compare_view.html_id, "figure"),
    Input("selected-countries-store", "data")
)
def update_compare_view(selected_countries):
    return compare_view.update(selected_countries)


# F. Radar Visibility Logic (Modified for Compare Mode and Explore Mode)
@app.callback(
    [Output("radar-state-store", "data"),
     Output(map_view.html_id, "clickData")],
    [Input(map_view.html_id, "clickData"),
     Input("close-radar-btn", "n_clicks")],
    [State("radar-state-store", "data"),
     State("compare-mode-store", "data"),
     State("explore-mode-store", "data")]
)
def toggle_radar_visibility(map_click, close_click, is_open, is_compare_mode, is_explore_mode):
    trigger = ctx.triggered_id
    if not trigger:
        return is_open, dash.no_update

    # If compare mode or explore mode is active, radar stays closed
    if is_compare_mode or is_explore_mode:
        return False, dash.no_update  # Changed from None to dash.no_update

    if trigger == "close-radar-btn":
        return False, None

    if trigger == map_view.html_id and map_click:
        return True, dash.no_update

    return is_open, dash.no_update


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




# H. Map Update (with Brushed and Selected Countries)
@app.callback(
    Output(map_view.html_id, "figure"),
    [Input("select-risk-variable", "value"),
     Input("explore-highlight-store", "data"),
     Input("selected-countries-store", "data"),
     Input("transport-selected-store", "data")]
)
def update_map(selected_risk, explore_highlight, selected_countries, transport_selected):
    explore_highlight = explore_highlight or []
    selected_countries = selected_countries or []
    transport_selected = transport_selected or []
    all_highlighted = list(set(explore_highlight + selected_countries + transport_selected))
    return map_view.update(selected_risk, all_highlighted)

# I. Radar Data Update
@app.callback(
    Output(radar_view.html_id, "figure"),
    [Input(map_view.html_id, "clickData"),
     Input("select-risk-variable", "value")]
)
def update_radar_data(click_data, selected_risk):
    country = click_data['points'][0]['location'] if click_data else None
    return radar_view.update(country, selected_risk)

@app.callback(
    Output("sim-anchor-country", "options"),
    Input("explore-mode-store", "data")
)
def load_anchor_options(explore_on):
    if not explore_on:
        return dash.no_update
    return [{"label": c, "value": c} for c in all_countries]





if __name__ == '__main__':
    app.run_server(debug=True)
