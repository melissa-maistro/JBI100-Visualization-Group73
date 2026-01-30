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

# --- INITIALIZATION ---
app = Dash(__name__)
app.title = "Humanitarian Risk Viz"

# Load data and initialize visualization views
df = get_data()
map_view = MapView("Map View", df)
radar_view = RadarView("Radar View", df)
compare_view = CompareView("Compare View", df)
transport_rank_view = TransportRankView("Transport Rank", df)

pca_scatter = Scatterplot(
    name="PCA Risk Space",
    feature_x="PC1",
    feature_y="PC2",
    df=df
)

# Configuration constants
all_countries = sorted(df['Country'].unique().tolist())
transport_slider_max = 25
transport_slider_marks = {5: "5", 10: "10", 15: "15", 20: "20", 25: "25"}

# --- CSS STYLES ---

# 1. Menu Drawer Style: Controls the invisible side navigation container
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

# 2. Radar/Detail Window Style: Floating panel on the right
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
    "transform": "translateX(130%)",  # Initially hidden off-screen
    "transition": "transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1)",
    "border": "1px solid rgba(230, 230, 235, 0.8)"
}

# 3. Hamburger Button Style
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

# 4. Backdrop Style: Dimmed background when menu/modals are open
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

# 5. Explore/PCA Drawer Style (Bottom Sheet)
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
    "whiteSpace": "nowrap",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "textAlign": "center"
}

# 7. Compare Search Panel (Floating dropdown)
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

# 8. Compare Drawer Style (Base style for dynamic height sheet)
COMPARE_SHEET_BASE_STYLE = {
    "position": "fixed",
    "bottom": "0",
    "left": "0",
    "width": "100vw",
    "height": "65vh",  # Default, overridden by state
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
SHEET_EXPANDED_HEIGHT = "70vh"

COMPARE_DRAWER_STYLE = COMPARE_SHEET_BASE_STYLE

# 9. Explore Button Style
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
    "whiteSpace": "nowrap",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "textAlign": "center"
}

# 10. Transport Button Style
TRANSPORT_BTN_STYLE = {
    "background": "linear-gradient(135deg, #f7971e 0%, #ffd200 100%)",
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
    "whiteSpace": "nowrap",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "textAlign": "center"
}

# 10.5 Top Button Row Container (Centers buttons)
TOP_BUTTON_ROW_STYLE = {
    "position": "fixed",
    "top": "25px",
    "left": "50%",
    "transform": "translateX(-50%)",  # Perfect centering
    "zIndex": 1800,
    "display": "flex",
    "gap": "14px",
    "alignItems": "center",
    "justifyContent": "center"
}

# 11. Transport Drawer Style (Right side panel)
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

# --- LAYOUT DEFINITION ---
app.layout = html.Div([
    # Client-side Stores (for state management without global variables)
    dcc.Store(id='menu-state-store', data=False),
    dcc.Store(id='radar-state-store', data=False),
    dcc.Store(id='pca-state-store', data=False),
    dcc.Store(id='brushed-countries-store', data={"countries": [], "source": None}),
    dcc.Store(id='compare-mode-store', data=False),
    dcc.Store(id='selected-countries-store', data=[]),
    dcc.Store(id='explore-mode-store', data=False),
    dcc.Store(id='explore-sheet-store', data='collapsed'),
    dcc.Store(id='compare-sheet-store', data='collapsed'),
    dcc.Store(id='transport-mode-store', data=False),
    dcc.Store(id='transport-selected-store', data=[]),
    dcc.Store(id='colorblind-state-store', data=False),

    # Overlay to capture clicks outside elements
    html.Div(
        id="click-capture-overlay",
        n_clicks=0,
        style={
            "position": "fixed",
            "top": 0, "left": 0, "width": "100vw", "height": "100vh",
            "zIndex": 0, "pointerEvents": "auto"
        }
    ),

    # Hamburger Menu & Backdrop
    html.Button("☰", id="hamburger-btn", n_clicks=0, style=HAMBURGER_STYLE),
    html.Div(id="menu-backdrop", style=BACKDROP_STYLE, n_clicks=0),

    # Main Action Buttons (Top Center)
    html.Div(
        id="top-action-buttons",
        style=TOP_BUTTON_ROW_STYLE,
        children=[
            html.Button("Compare Countries", id="compare-btn", n_clicks=0, style=COMPARE_BTN_STYLE),
            html.Button("Explore Correlations", id="explore-btn", n_clicks=0, style=EXPLORE_BTN_STYLE),
            html.Button("TRANSPORT FOCUS", id="transport-btn", n_clicks=0, style=TRANSPORT_BTN_STYLE),
        ]
    ),

    # --- DRAWER COMPONENTS ---

    # 1. Compare Mode Components
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

    html.Div(id="compare-drawer", style=COMPARE_DRAWER_STYLE, children=[
        html.Div(
            style={
                "display": "flex", "justifyContent": "space-between", "alignItems": "center",
                "marginBottom": "16px", "paddingBottom": "12px",
                "borderBottom": "2px solid rgba(102, 126, 234, 0.2)"
            },
            children=[
                html.H5("Risk Comparison", style={"margin": 0, "color": "#2c3e50"}),
                html.Div(
                    style={"display": "flex", "gap": "10px", "alignItems": "center"},
                    children=[
                        # RESTORED STYLES FOR FOCUS BUTTONS
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

    # 2. Explore Mode Components (PCA)
    html.Div(id="explore-drawer", style=PCA_CONTAINER_STYLE, children=[
        # Header
        html.Div(
            style={
                "display": "flex", "justifyContent": "space-between", "alignItems": "center",
                "marginBottom": "16px", "paddingBottom": "12px",
                "borderBottom": "2px solid rgba(17, 153, 142, 0.2)"
            },
            children=[
                html.H5("PCA Risk Space - Explore Correlations", style={"margin": 0, "color": "#2c3e50"}),
                html.Div(
                    style={"display": "flex", "gap": "10px", "alignItems": "center"},
                    children=[
                        # RESTORED STYLES FOR FOCUS BUTTONS (Green Theme)
                        html.Button(
                            "Focus Map",
                            id="focus-map-explore-btn",
                            n_clicks=0,
                            style={
                                "background": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
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
                            id="focus-plot-explore-btn",
                            n_clicks=0,
                            style={
                                "background": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
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
                            id="close-explore-btn",
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

        # Graph Container (Updated to use Flexbox to fill available space)
        html.Div(
            dcc.Graph(
                id=pca_scatter.html_id,
                figure=pca_scatter.update('rgb(255,100,100)', None),
                style={"height": "100%", "width": "100%"}  # Fills the flex container
            ),
            style={"flex": "1", "overflow": "hidden", "position": "relative"}
        ),

        # --- PCA LEGEND & METHODOLOGY ---
        html.Div(
            style={
                "padding": "12px 15px",
                "backgroundColor": "#f8f9fa",
                "borderTop": "1px solid #e9ecef",
                "fontSize": "12px",
                "color": "#495057",
                "flexShrink": 0
            },
            children=[
                html.Strong("Methodology Note:"),
                html.Span(
                    " The graph reduces the 5 dimensions of risk (Economic, Social, Infrastructure, Demographic, Transport) into 2 coordinates (PC1, PC2). "
                    "Closer points indicate countries with similar risk profiles."
                )
            ]
        )
    ]),

    # 3. Transport Drawer
    html.Div(id="transport-drawer", style=TRANSPORT_DRAWER_STYLE, children=[
        html.Div(
            style={"marginBottom": "12px", "borderBottom": "2px solid rgba(247, 151, 30, 0.25)"},
            children=[html.H5("Transport Intervention Finder", style={"color": "#2c3e50"})]
        ),
        html.Div(
            className="js-no-drag",
            children=[
                html.Label("Show top N constrained countries:", style={"fontSize": "12px", "color": "#555"}),
                dcc.Slider(
                    id="transport-topn-slider",
                    min=5, max=transport_slider_max, step=5, value=15,
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

    # 4. Left Menu Drawer
    html.Div(
        id="menu-drawer",
        style=MENU_CONTAINER_STYLE,
        children=[
            html.Div(children=[make_menu_layout()], style={"minWidth": "300px"})
        ]
    ),

    # 5. Radar Detail Drawer (Right side)
    html.Div(
        id="radar-drawer",
        style=RADAR_CONTAINER_STYLE,
        children=[
            html.Div(
                id="radar-header",
                style={
                    "display": "flex", "justifyContent": "space-between", "alignItems": "center",
                    "marginBottom": "16px", "cursor": "move",
                    "borderBottom": "2px solid rgba(100, 149, 237, 0.2)"
                },
                children=[
                    html.H5("Country Details", style={"margin": 0, "color": "#2c3e50"}),
                    html.Button("×", id="close-radar-btn", n_clicks=0,
                                style={"background": "transparent", "border": "none", "fontSize": "28px"})
                ]
            ),
            html.Div(radar_view, style={"flex": "1"})
        ]
    ),

    # Background Map
    html.Div(
        style={
            "height": "100vh", "width": "100vw",
            "position": "absolute", "top": 0, "left": 0, "zIndex": 1
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
    """
    Toggles the Menu State (Boolean).
    Closes menu if a risk variable is selected or backdrop is clicked.
    """
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
    """
    Updates CSS to show/hide the menu drawer based on state.
    """
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


# B. Compare Mode Logic
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
     State("explore-mode-store", "data"),
     State("transport-mode-store", "data")]
)
def compare_controller(n_compare, n_close, n_focus_map, n_focus_plot, is_active, sheet_state, explore_mode,
                       transport_mode):
    """
    Manages the Compare Mode lifecycle.
    1. Toggles activation (blocks if other modes are active).
    2. Handles 'Focus Map' (collapsed sheet) vs 'Focus Plot' (expanded sheet).
    3. Resets country selection on close.
    """
    trigger = ctx.triggered_id
    if not trigger:
        return (dash.no_update,) * 7

    search_style = COMPARE_PANEL_STYLE.copy()
    drawer_style = COMPARE_SHEET_BASE_STYLE.copy()
    btn_style = COMPARE_BTN_STYLE.copy()

    new_sheet_state = sheet_state or "collapsed"

    # CASE 1: Close button clicked
    if trigger == "close-compare-btn":
        search_style["display"] = "none"
        drawer_style["display"] = "none"
        drawer_style["height"] = SHEET_COLLAPSED_HEIGHT
        btn_style["background"] = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        return False, search_style, drawer_style, btn_style, "Compare Countries", [], "collapsed"

    # CASE 2: Main Toggle button clicked
    if trigger == "compare-btn":
        if (explore_mode or transport_mode) and not is_active:
            return (dash.no_update,) * 7
        new_state = not is_active
        if new_state:
            # Open: Show panel + sheet (collapsed by default)
            search_style["display"] = "block"
            drawer_style["display"] = "block"
            drawer_style["height"] = SHEET_COLLAPSED_HEIGHT
            btn_style["background"] = "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)"
            return True, search_style, drawer_style, btn_style, "Stop Comparing", dash.no_update, "collapsed"
        else:
            # Close
            search_style["display"] = "none"
            drawer_style["display"] = "none"
            drawer_style["height"] = SHEET_COLLAPSED_HEIGHT
            btn_style["background"] = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
            return False, search_style, drawer_style, btn_style, "Compare Countries", [], "collapsed"

    # CASE 3: Focus buttons (Sheet resizing)
    if not is_active:
        return (dash.no_update,) * 7

    if trigger == "focus-plot-btn":
        new_sheet_state = "expanded"
    elif trigger == "focus-map-btn":
        new_sheet_state = "collapsed"

    drawer_style["display"] = "block"
    drawer_style["height"] = SHEET_EXPANDED_HEIGHT if new_sheet_state == "expanded" else SHEET_COLLAPSED_HEIGHT

    search_style["display"] = "block"
    btn_style["background"] = "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)"
    return True, search_style, drawer_style, btn_style, "Stop Comparing", dash.no_update, new_sheet_state


# B2. Explore Mode Logic
@app.callback(
    [Output("explore-mode-store", "data"),
     Output("explore-drawer", "style"),
     Output("explore-btn", "style"),
     Output("explore-btn", "children"),
     Output("explore-sheet-store", "data")],
    [Input("explore-btn", "n_clicks"),
     Input("close-explore-btn", "n_clicks"),
     Input("focus-map-explore-btn", "n_clicks"),
     Input("focus-plot-explore-btn", "n_clicks")],
    [State("explore-mode-store", "data"),
     State("compare-mode-store", "data"),
     State("explore-sheet-store", "data"),
     State("transport-mode-store", "data")]
)
def explore_controller(n_explore, n_close, n_map, n_plot, is_active, compare_mode, sheet_state, transport_mode):
    """
    Manages Explore Mode (PCA) lifecycle.
    Similar to Compare Mode, but defaults to 'Expanded' on open for better plot visibility.
    """
    trigger = ctx.triggered_id
    if not trigger:
        return (dash.no_update,) * 5

    drawer_style = PCA_CONTAINER_STYLE.copy()
    btn_style = EXPLORE_BTN_STYLE.copy()
    btn_style.update({"display": "flex", "alignItems": "center", "justifyContent": "center", "textAlign": "center"})

    new_sheet_state = sheet_state or "collapsed"

    # Close
    if trigger == "close-explore-btn":
        drawer_style["display"] = "none"
        drawer_style["height"] = SHEET_COLLAPSED_HEIGHT
        return False, drawer_style, btn_style, "Explore Correlations", "collapsed"

    # Toggle
    if trigger == "explore-btn":
        if (compare_mode or transport_mode) and not is_active:
            return (dash.no_update,) * 5

        new_active = not is_active
        if new_active:
            # Open directly in Expanded mode
            drawer_style["display"] = "flex"
            drawer_style["flexDirection"] = "column"
            drawer_style["height"] = SHEET_EXPANDED_HEIGHT
            btn_style["background"] = "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)"
            return True, drawer_style, btn_style, "Close Explorer", "expanded"
        else:
            drawer_style["display"] = "none"
            return False, drawer_style, btn_style, "Explore Correlations", "collapsed"

    # Focus Logic
    if not is_active:
        return (dash.no_update,) * 5

    if trigger == "focus-plot-explore-btn":
        new_sheet_state = "expanded"
    elif trigger == "focus-map-explore-btn":
        new_sheet_state = "collapsed"

    drawer_style["display"] = "flex"
    drawer_style["flexDirection"] = "column"
    drawer_style["height"] = SHEET_EXPANDED_HEIGHT if new_sheet_state == "expanded" else SHEET_COLLAPSED_HEIGHT
    btn_style["background"] = "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)"

    return dash.no_update, drawer_style, btn_style, "Close Explorer", new_sheet_state


# B3. Transport Mode Logic
@app.callback(
    [Output("transport-mode-store", "data"),
     Output("transport-drawer", "style"),
     Output("transport-btn", "style"),
     Output("transport-btn", "children")],
    [Input("transport-btn", "n_clicks")],
    [State("transport-mode-store", "data"),
     State("compare-mode-store", "data"),
     State("explore-mode-store", "data")]
)
def toggle_transport_mode(btn_click, is_active, compare_mode, explore_mode):
    """
    Toggles the Transport Intervention Finder drawer.
    Mutually exclusive with Compare and Explore modes.
    """
    trigger = ctx.triggered_id
    if not trigger:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    if (compare_mode or explore_mode) and not is_active:
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
        return False, drawer_style, TRANSPORT_BTN_STYLE, "TRANSPORT FOCUS"


# B4. Transport Rank Update
@app.callback(
    Output(transport_rank_view.html_id, "figure"),
    [Input("transport-topn-slider", "value"),
     Input("transport-selected-store", "data")]
)
def update_transport_rank(top_n, selected_countries):
    """Updates the Bar Chart based on Slider value and selection."""
    return transport_rank_view.update(top_n=top_n, selected_countries=selected_countries)


# B5. Transport Selection
@app.callback(
    Output("transport-selected-store", "data"),
    [Input(transport_rank_view.html_id, "clickData"),
     Input("transport-mode-store", "data")],
    [State("transport-selected-store", "data")]
)
def update_transport_selection(click_data, transport_mode, selected_countries):
    """Handles clicking on the Transport bar chart to select a country."""
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


# C. Manage Country Selection (Dropdown + Map Interaction)
@app.callback(
    Output("country-selector", "value"),
    [Input(map_view.html_id, "clickData"),
     Input("country-selector", "value"),
     Input("compare-mode-store", "data")]
)
def manage_selection_ui(map_click, dropdown_value, compare_mode):
    """
    Syncs the Dropdown value with Map clicks.
    Only active when Compare Mode is ON.
    """
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

        # Toggle selection
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


# F. Radar Visibility Logic
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
    """
    Shows/Hides the Country Details (Radar) side panel.
    - Opens on Map click.
    - Disabled if Compare or Explore mode is active.
    """
    if not ctx.triggered:
        return is_open, dash.no_update

    triggered_ids = {t["prop_id"].split(".")[0] for t in ctx.triggered}

    if is_compare_mode or is_explore_mode:
        return False, dash.no_update

    if "close-radar-btn" in triggered_ids:
        return False, None

    if map_view.html_id in triggered_ids and map_click:
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
        style["display"] = "flex"
    else:
        style["transform"] = "translateX(130%)"
        style["display"] = "none"
    return style


# G. Store Brushed Countries from PCA (Brushing & Linking)
@app.callback(
    Output("brushed-countries-store", "data", allow_duplicate=True),
    [Input(pca_scatter.html_id, "selectedData"),
     Input("explore-mode-store", "data")],
    [State("explore-mode-store", "data")],
    prevent_initial_call=True
)
def store_brushed_countries(selected_data, explore_mode_change, explore_mode_state):
    """
    Updates the list of highlighted countries based on lasso/box selection in PCA plot.
    """
    trigger = ctx.triggered_id

    if trigger == "explore-mode-store" and not explore_mode_state:
        return {"countries": [], "source": "clear"}

    if trigger == pca_scatter.html_id:
        if not selected_data or 'points' not in selected_data or not selected_data['points']:
            return dash.no_update

        selected_indices = [point['pointIndex'] for point in selected_data['points']]
        brushed_countries = df.iloc[selected_indices]['Country'].tolist() if 'Country' in df.columns else []

        return {"countries": brushed_countries, "source": "pca"}

    return dash.no_update


# G2. Store Brushed Countries from Map Clicks (Explore Mode)
@app.callback(
    Output("brushed-countries-store", "data", allow_duplicate=True),
    [Input(map_view.html_id, "clickData"),
     Input("explore-mode-store", "data")],
    [State("brushed-countries-store", "data"),
     State("explore-mode-store", "data")],
    prevent_initial_call=True
)
def store_brushed_from_map(map_click, explore_mode_change, brushed_countries, explore_mode_state):
    """
    Allows selecting countries on the map to highlight them in the PCA plot (Bi-directional linking).
    """
    trigger = ctx.triggered_id

    if trigger == "explore-mode-store" and not explore_mode_state:
        return {"countries": [], "source": "clear"}

    if trigger != map_view.html_id:
        return dash.no_update

    if not explore_mode_state or not map_click:
        return dash.no_update

    country = map_click["points"][0].get("location")
    if not country:
        return dash.no_update

    if isinstance(brushed_countries, dict):
        current = brushed_countries.get("countries", [])
    else:
        current = brushed_countries or []

    if country in current:
        updated = [c for c in current if c != country]
    else:
        updated = current + [country]
    return {"countries": updated, "source": "map"}


# H. Main Map Update
@app.callback(
    Output(map_view.html_id, "figure"),
    [Input("select-risk-variable", "value"),
     Input("brushed-countries-store", "data"),
     Input("selected-countries-store", "data"),
     Input("transport-selected-store", "data"),
     Input("colorblind-mode", "value")]
)
def update_map(selected_risk, brushed_countries, selected_countries, transport_selected, cb_value):
    """
    Redraws the map based on:
    1. Selected risk variable.
    2. Highlights from PCA brushing, Compare selection, or Transport selection.
    3. Colorblind mode setting.
    """
    is_colorblind = True if cb_value and 'active' in cb_value else False

    if isinstance(brushed_countries, dict):
        brushed_list = brushed_countries.get("countries", [])
    else:
        brushed_list = brushed_countries or []

    all_highlighted = list(set(brushed_list + selected_countries + transport_selected))

    return map_view.update(selected_risk, all_highlighted, is_colorblind)


# I. Radar Data Update
@app.callback(
    Output(radar_view.html_id, "figure"),
    [Input(map_view.html_id, "clickData"),
     Input("select-risk-variable", "value")]
)
def update_radar_data(click_data, selected_risk):
    if not click_data:
        return dash.no_update
    country = click_data['points'][0]['location']
    return radar_view.update(country, selected_risk)


# J. PCA Graph Update (Visualization Synchronization)
@app.callback(
    Output(pca_scatter.html_id, "figure"),
    [Input("explore-mode-store", "data"),
     Input("brushed-countries-store", "data")]
)
def update_pca_graph(explore_mode, brushed_countries):
    """
    Updates PCA Scatterplot to highlight countries selected on the map.
    Prevents circular update if source is PCA itself.
    """
    trigger = ctx.triggered_id

    if not explore_mode:
        return dash.no_update

    source = None
    if isinstance(brushed_countries, dict):
        brushed_list = brushed_countries.get("countries", [])
        source = brushed_countries.get("source")
    else:
        brushed_list = brushed_countries or []

    # If selection originated from PCA, do not redraw (preserves selection tool state)
    if trigger == "brushed-countries-store" and source == "pca":
        return dash.no_update

    selected_color = "rgb(17, 153, 142)"
    selected_indices = None
    if brushed_list:
        selected_indices = df[df["Country"].isin(brushed_list)].index.tolist()

    return pca_scatter.update(selected_color, selected_indices)


# K. Methodology Info (Optional)
@app.callback(
    [Output("info-card", "style"),
     Output("info-backdrop", "style")],
    [Input("open-info-btn", "n_clicks"),
     Input("info-backdrop", "n_clicks")],
    [State("info-card", "style"),
     State("info-backdrop", "style")]
)
def toggle_methodology_info(n_open, n_backdrop, card_style, backdrop_style):
    trigger = ctx.triggered_id

    if trigger == "open-info-btn" and n_open > 0:
        card_style["display"] = "block"
        backdrop_style["display"] = "block"
    elif trigger == "info-backdrop":
        card_style["display"] = "none"
        backdrop_style["display"] = "none"

    return card_style, backdrop_style


if __name__ == '__main__':
    app.run_server(debug=True)