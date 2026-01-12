from dash import dcc, html


def generate_description_card():
    return html.Div(
        id="description-card",
        children=[
            html.H5("JBI100 - Group 73", style={'marginTop': '0px'}),  # Riduco margine
            html.H3("Humanitarian Risk", style={'marginBottom': '10px'}),  # Titolo più compatto
            html.Div(
                id="intro",
                children="Select a risk dimension to visualize.",
                style={'fontSize': '14px', 'marginBottom': '15px'}  # Testo più piccolo
            ),
        ],
    )


def generate_control_card():
    return html.Div(
        id="control-card",
        children=[
            html.Label("Select Risk Layer", style={'fontWeight': 'bold', 'fontSize': '14px', 'marginBottom': '10px'}),
            dcc.RadioItems(
                id="select-risk-variable",
                options=[
                    {'label': ' Total Vulnerability Index', 'value': 'Total Vulnerability'},
                    {'label': ' Economic Resilience', 'value': 'Economic Risk'},
                    {'label': ' Social Fragility', 'value': 'Social Risk'},
                    {'label': ' Infrastructure Constraints', 'value': 'Infrastructure Risk'},
                    {'label': ' Demographic Stress', 'value': 'Demographic Risk'}
                ],
                value='Total Vulnerability',
                # 'display': 'block' mette ogni opzione su una nuova riga
                labelStyle={'display': 'block', 'marginBottom': '8px', 'fontSize': '13px'},
                style={'marginTop': '10px'}
            ),
        ],
    )


def make_menu_layout():
    return html.Div(
        id="floating-menu",
        children=[
            generate_description_card(),
            html.Hr(style={'margin': '15px 0'}), # Una linea separatrice elegante
            generate_control_card(),
        ],
        style={
            'position': 'absolute',
            'top': '20px',
            'left': '20px',
            'zIndex': '1000',
            'width': '280px',         # Leggermente più stretto per eleganza
            'backgroundColor': 'rgba(255, 255, 255, 0.95)', # Più opaco per leggere meglio il testo
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 4px 15px rgba(0,0,0,0.2)',
            'height': 'auto',         # FONDAMENTALE: si adatta al contenuto
            'maxHeight': '90vh',      # Limite massimo di sicurezza
        }
    )