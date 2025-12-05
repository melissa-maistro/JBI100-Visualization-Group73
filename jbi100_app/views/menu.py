from dash import dcc, html

def generate_description_card():
    return html.Div(
        id="description-card",
        children=[
            html.H5("Humanitarian Analytics"),
            html.H3("Vulnerability Dashboard"),
            html.Div(
                id="intro",
                children="Explore structural risks across countries. Select a risk dimension below and click on the map for details.",
            ),
        ],
    )

def generate_control_card():
    return html.Div(
        id="control-card",
        children=[
            html.Label("Select Risk Dimension"),
            dcc.Dropdown(
                id="select-risk-variable",
                options=[
                    {'label': 'Total Vulnerability', 'value': 'Total Vulnerability'},
                    {'label': 'Economic Risk', 'value': 'Economic Risk'},
                    {'label': 'Demographic Risk', 'value': 'Demographic Risk'},
                    {'label': 'Infrastructure Risk', 'value': 'Infrastructure Risk'},
                    {'label': 'Social Risk', 'value': 'Social Risk'}
                ],
                value='Total Vulnerability',
                clearable=False
            ),
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