from dash import dcc, html

def generate_description_card():
    return html.Div(
        id="description-card",
        children=[
            html.H5("JBI100 - Group 73"),
            html.H3("Humanitarian Risk Dashboard"),
            html.Div(
                id="intro",
                children="Select a risk dimension to visualize on the map. Click on a country to see the detailed risk breakdown.",
            ),
        ],
    )

def generate_control_card():
    return html.Div(
        id="control-card",
        children=[
            html.Label("Select Risk Layer"),
            dcc.Dropdown(
                id="select-risk-variable",
                options=[
                    {'label': 'Total Vulnerability Index', 'value': 'Total Vulnerability'},
                    {'label': 'Economic Resilience', 'value': 'Economic Risk'},
                    {'label': 'Social Fragility', 'value': 'Social Risk'},
                    {'label': 'Infrastructure Constraints', 'value': 'Infrastructure Risk'},
                    {'label': 'Demographic Stress', 'value': 'Demographic Risk'}
                ],
                value='Total Vulnerability',
                clearable=False
            ),

            html.Hr(),

            html.H4("Task 2 — Compare Countries", style={"marginTop": "10px"}),

            html.Label("Dimensions to compare"),
            dcc.Checklist(
                id="compare-dimensions",
                options=[
                    {"label": "Economic", "value": "Economic Risk"},
                    {"label": "Social", "value": "Social Risk"},
                    {"label": "Infrastructure", "value": "Infrastructure Risk"},
                    {"label": "Demographic", "value": "Demographic Risk"},
                ],
                value=["Economic Risk", "Social Risk", "Infrastructure Risk", "Demographic Risk"],
            ),

            html.Label("Countries (multi-select)"),
            dcc.Dropdown(
                id="compare-countries",
                options=[],           # riempito via callback
                value=[],
                multi=True,
                placeholder="Select countries or click on the map to add",
            ),

            html.Button("Clear comparison", id="clear-compare", n_clicks=0, style={"marginTop": "8px"}),

            # memoria dello stato (lista paesi in confronto)
            dcc.Store(id="compare-store", data=[]),
        ],
    )

def make_menu_layout():
    return html.Div(
        id="left-column",
        className="four columns",
        children=[
            generate_description_card(),
            generate_control_card(),
        ],
    )