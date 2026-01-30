from dash import dcc, html


def generate_description_card():
    """
    Generates the header section of the menu (Title and short intro).
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("JBI100 - Group 73", style={'marginTop': '0px', 'paddingRight': '30px'}),
            html.H3("Humanitarian Risk", style={'marginBottom': '10px'}),
            html.Div(
                id="intro",
                children="Select a risk dimension to visualize.",
                style={'fontSize': '14px', 'marginBottom': '15px'}
            ),
        ],
    )


def generate_control_card():
    """
    Generates the control section containing:
    1. Radio buttons to select the Risk Variable.
    2. Checklist to toggle Colorblind Mode.
    """
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
                    {'label': ' Demographic Stress', 'value': 'Demographic Risk'},
                    {'label': ' Transport Constraint (Intervention)', 'value': 'Transport Constraint'}
                ],
                value='Total Vulnerability',
                labelStyle={'display': 'block', 'marginBottom': '8px', 'fontSize': '13px'},
                style={'marginTop': '10px'}
            ),

            # --- ACCESSIBILITY SECTION ---
            html.Hr(style={'margin': '20px 0'}),
            html.Label("Accessibility", style={'fontWeight': 'bold', 'fontSize': '14px', 'marginBottom': '10px'}),
            dcc.Checklist(
                id="colorblind-mode",
                options=[{'label': ' Colorblind Friendly Mode', 'value': 'active'}],
                value=[],
                style={'fontSize': '13px', 'marginTop': '5px'}
            ),
        ],
    )


def generate_info_tooltip():
    """
    Creates the 'Methodology' tooltip with a click-away backdrop.
    Uses 'position: fixed' with negative coordinates to ensure the backdrop
    covers the entire screen even if parent elements have CSS transforms.
    """

    # 1. Invisible Backdrop Style
    # Huge negative margins ensure it captures clicks outside the menu context
    backdrop_style = {
        'position': 'fixed',
        'top': '-100vh',
        'left': '-100vw',
        'width': '300vw',  # Much larger than viewport
        'height': '300vh',
        'zIndex': 2998,
        'display': 'none',  # Hidden initially
        'cursor': 'default',
        'backgroundColor': 'transparent'
    }

    # 2. Tooltip Card Style
    card_style = {
        'position': 'absolute',
        'top': '-10px',
        'left': '45px',
        'width': '260px',
        'backgroundColor': 'white',
        'border': '1px solid #ccc',
        'borderRadius': '8px',
        'padding': '15px',
        'fontSize': '12px',
        'fontFamily': 'Arial, sans-serif',
        'color': '#333',
        'boxShadow': '0 4px 20px rgba(0,0,0,0.3)',
        'zIndex': 2999,
        'textAlign': 'left',
        'display': 'none'  # Hidden initially
    }

    return html.Div([
        # Backdrop to handle closing when clicking outside
        html.Div(id="info-backdrop", style=backdrop_style, n_clicks=0),

        # Button + Card Wrapper
        html.Div(
            style={
                'position': 'absolute',
                'top': '15px',
                'right': '15px',
                'zIndex': 3000
            },
            children=[
                # The "?" Button
                html.Div(
                    "?",
                    id="open-info-btn",
                    n_clicks=0,
                    style={
                        'width': '24px', 'height': '24px',
                        'backgroundColor': '#eee', 'color': '#555',
                        'textAlign': 'center', 'lineHeight': '24px',
                        'fontWeight': 'bold', 'borderRadius': '50%',
                        'cursor': 'pointer', 'border': '1px solid #ccc',
                        'userSelect': 'none'
                    },
                    title="Show Methodology"
                ),

                # The Content Card
                html.Div(
                    id="info-card",
                    style=card_style,
                    children=[
                        html.H5("Methodology", style={'margin': '0 0 10px 0', 'color': '#007bff'}),

                        html.Div([
                            html.B("💰 Economic"),
                            html.Ul([
                                html.Li("Poverty, Debt (+)"),
                                html.Li("GDP per Capita (Inv)")
                            ], style={'paddingLeft': '15px', 'margin': '2px 0 8px 0'})
                        ]),

                        html.Div([
                            html.B("👫 Social"),
                            html.Ul([
                                html.Li("Infant Mort., Youth Unemp. (+)"),
                                html.Li("Net Migration (Inv)")
                            ], style={'paddingLeft': '15px', 'margin': '2px 0 8px 0'})
                        ]),

                        html.Div([
                            html.B("🏗️ Infrastructure"),
                            html.Ul([
                                html.Li("Elec., Roads, Internet (Inv)")
                            ], style={'paddingLeft': '15px', 'margin': '2px 0 8px 0'})
                        ]),

                        html.Div([
                            html.B("📉 Demographic"),
                            html.Ul([
                                html.Li("Growth (+), Median Age (Inv)")
                            ], style={'paddingLeft': '15px', 'margin': '2px 0 0 0'})
                        ]),

                        html.Div([
                            html.B("🛣️ Transport Intervention"),
                            html.Ul([
                                html.Li("Runways (paved + unpaved), Roads, Railways, Waterways"),
                                html.Li("Density per population/area → log + normalize"),
                                html.Li("Constraint = 1 − Supply (higher = worse)")
                            ], style={'paddingLeft': '15px', 'margin': '2px 0 0 0'})
                        ]),

                        html.Div("Click anywhere else to close",
                                 style={'fontSize': '10px', 'color': '#aaa', 'marginTop': '10px', 'textAlign': 'right',
                                        'fontStyle': 'italic'})
                    ]
                )
            ]
        )
    ])


def make_menu_layout():
    """
    Assembles the main floating menu.
    """
    return html.Div(
        id="floating-menu",
        children=[
            generate_info_tooltip(),
            generate_description_card(),
            html.Hr(style={'margin': '15px 0'}),
            generate_control_card(),
        ],
        style={
            'position': 'absolute',
            'top': '20px',
            'left': '20px',
            'zIndex': '1000',
            'width': '280px',
            'backgroundColor': 'rgba(255, 255, 255, 0.95)',
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 4px 15px rgba(0,0,0,0.2)',
            'height': 'auto',
            'maxHeight': '90vh',
        }
    )