# jbi100_app/views/explore_panel.py
from dash import dcc, html
from dash import dash_table


class ExplorePanel(html.Div):
    """
    Explore Panel con due tab:
    - Similarity: anchor -> topK similari
    - Clustering: kmeans(K) + cluster selection
    """
    def __init__(self, name="Explore Panel"):
        self.html_id = name.lower().replace(" ", "-")

        super().__init__(
            id=self.html_id,
            children=[
                dcc.Tabs(
                    id="explore-tabs",
                    value="tab-similarity",
                    children=[
                        dcc.Tab(
                            label="Similarity Explorer",
                            value="tab-similarity",
                            children=[
                                html.Div(
                                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "14px",
                                           "marginTop": "14px"},
                                    children=[
                                        html.Div([
                                            html.Label("Anchor country", style={"fontSize": "12px", "color": "#555"}),
                                            dcc.Dropdown(
                                                id="sim-anchor-country",
                                                placeholder="Select an anchor country...",
                                                clearable=True
                                            ),
                                        ]),
                                        html.Div([
                                            html.Label("Top-K similar", style={"fontSize": "12px", "color": "#555"}),
                                            dcc.Slider(
                                                id="sim-topk",
                                                min=3, max=15, step=1, value=7,
                                                marks={3: "3", 7: "7", 10: "10", 15: "15"},
                                                tooltip={"placement": "bottom", "always_visible": False}
                                            ),
                                        ]),
                                    ],
                                ),

                                html.Div(
                                    style={"marginTop": "10px"},
                                    children=[
                                        html.Label("Dimensions used", style={"fontSize": "12px", "color": "#555"}),
                                        dcc.Checklist(
                                            id="sim-dims",
                                            value=["Economic Risk", "Social Risk", "Infrastructure Risk", "Demographic Risk"],
                                            options=[
                                                {"label": " Economic", "value": "Economic Risk"},
                                                {"label": " Social", "value": "Social Risk"},
                                                {"label": " Infrastructure", "value": "Infrastructure Risk"},
                                                {"label": " Demographic", "value": "Demographic Risk"},
                                            ],
                                            style={"display": "flex", "gap": "18px", "flexWrap": "wrap", "marginTop": "6px"},
                                        ),
                                    ],
                                ),

                                html.Div(
                                    style={"display": "flex", "gap": "10px", "marginTop": "12px"},
                                    children=[
                                        html.Button(
                                            "Use selection in Compare",
                                            id="sim-send-to-compare",
                                            n_clicks=0,
                                            style={
                                                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                                "color": "white",
                                                "border": "none",
                                                "padding": "8px 14px",
                                                "borderRadius": "18px",
                                                "cursor": "pointer",
                                                "fontSize": "12px",
                                                "fontWeight": "600"
                                            }
                                        ),
                                    ],
                                ),

                                html.Div(
                                    style={"display": "grid", "gridTemplateColumns": "1.1fr 1fr", "gap": "16px",
                                           "marginTop": "14px"},
                                    children=[
                                        dash_table.DataTable(
                                            id="sim-table",
                                            columns=[
                                                {"name": "Country", "id": "Country"},
                                                {"name": "Distance", "id": "Distance"},
                                            ],
                                            data=[],
                                            page_size=8,
                                            style_table={"height": "260px", "overflowY": "auto"},
                                            style_cell={
                                                "fontFamily": "Arial",
                                                "fontSize": "12px",
                                                "padding": "6px",
                                                "whiteSpace": "nowrap",
                                                "overflow": "hidden",
                                                "textOverflow": "ellipsis"
                                            },
                                            style_header={"fontWeight": "700", "backgroundColor": "#f5f6fa"},
                                        ),
                                        dcc.Graph(
                                            id="sim-delta-bar",
                                            config={"displayModeBar": False},
                                            style={"height": "280px"},
                                        ),
                                    ],
                                )
                            ],
                        ),

                        dcc.Tab(
                            label="Clustering Explorer",
                            value="tab-clustering",
                            children=[
                                html.Div(
                                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "14px",
                                           "marginTop": "14px"},
                                    children=[
                                        html.Div([
                                            html.Label("Number of clusters (K)", style={"fontSize": "12px", "color": "#555"}),
                                            dcc.Slider(
                                                id="clust-k",
                                                min=2, max=8, step=1, value=4,
                                                marks={2: "2", 4: "4", 6: "6", 8: "8"},
                                                tooltip={"placement": "bottom", "always_visible": False}
                                            ),
                                        ]),
                                        html.Div([
                                            html.Label("Dimensions used", style={"fontSize": "12px", "color": "#555"}),
                                            dcc.Checklist(
                                                id="clust-dims",
                                                value=["Economic Risk", "Social Risk", "Infrastructure Risk", "Demographic Risk"],
                                                options=[
                                                    {"label": " Economic", "value": "Economic Risk"},
                                                    {"label": " Social", "value": "Social Risk"},
                                                    {"label": " Infrastructure", "value": "Infrastructure Risk"},
                                                    {"label": " Demographic", "value": "Demographic Risk"},
                                                ],
                                                style={"display": "flex", "gap": "18px", "flexWrap": "wrap", "marginTop": "6px"},
                                            ),
                                        ]),
                                    ],
                                ),

                                html.Div(
                                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "14px",
                                           "marginTop": "12px"},
                                    children=[
                                        html.Div([
                                            html.Label("Select cluster", style={"fontSize": "12px", "color": "#555"}),
                                            dcc.Dropdown(
                                                id="clust-select",
                                                placeholder="Select a cluster...",
                                                clearable=True
                                            ),
                                        ]),
                                        html.Div(
                                            style={"display": "flex", "gap": "10px", "alignItems": "end"},
                                            children=[
                                                html.Button(
                                                    "Use cluster in Compare",
                                                    id="clust-send-to-compare",
                                                    n_clicks=0,
                                                    style={
                                                        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                                        "color": "white",
                                                        "border": "none",
                                                        "padding": "8px 14px",
                                                        "borderRadius": "18px",
                                                        "cursor": "pointer",
                                                        "fontSize": "12px",
                                                        "fontWeight": "600"
                                                    }
                                                ),
                                            ],
                                        ),
                                    ],
                                ),

                                html.Div(
                                    style={"display": "grid", "gridTemplateColumns": "1.1fr 1fr", "gap": "16px",
                                           "marginTop": "14px"},
                                    children=[
                                        dash_table.DataTable(
                                            id="clust-table",
                                            columns=[
                                                {"name": "Cluster", "id": "Cluster"},
                                                {"name": "Size", "id": "Size"},
                                            ],
                                            data=[],
                                            page_size=8,
                                            style_table={"height": "260px", "overflowY": "auto"},
                                            style_cell={
                                                "fontFamily": "Arial",
                                                "fontSize": "12px",
                                                "padding": "6px",
                                                "whiteSpace": "nowrap",
                                                "overflow": "hidden",
                                                "textOverflow": "ellipsis"
                                            },
                                            style_header={"fontWeight": "700", "backgroundColor": "#f5f6fa"},
                                        ),
                                        dcc.Graph(
                                            id="clust-explain-bar",
                                            config={"displayModeBar": False},
                                            style={"height": "280px"},
                                        ),
                                    ],
                                ),

                                html.Div(
                                    style={"marginTop": "10px"},
                                    children=[
                                        html.Label("Countries in selected cluster", style={"fontSize": "12px", "color": "#555"}),
                                        dash_table.DataTable(
                                            id="clust-countries",
                                            columns=[{"name": "Country", "id": "Country"}],
                                            data=[],
                                            page_size=8,
                                            style_table={"height": "240px", "overflowY": "auto"},
                                            style_cell={"fontFamily": "Arial", "fontSize": "12px", "padding": "6px"},
                                            style_header={"fontWeight": "700", "backgroundColor": "#f5f6fa"},
                                        )
                                    ],
                                )
                            ],
                        ),
                    ]
                )
            ]
        )