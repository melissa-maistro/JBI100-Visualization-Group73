from dash import dcc, html


def generate_description_card():
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
                labelStyle={'display': 'block', 'marginBottom': '8px', 'fontSize': '13px'},
                style={'marginTop': '10px'}
            ),
        ],
    )


def generate_compare_controls():
    """
    Controlli per la modalità di comparazione tra paesi.
    IMPORTANTE: Usa ID diversi se ci sono duplicati
    """
    return html.Div(
        id="compare-section",
        children=[
            html.Hr(style={'margin': '15px 0'}),
            
            # Bottone per attivare/disattivare la modalità compare
            html.Button(
                "Activate Compare Mode",
                id="toggle-compare-btn",
                n_clicks=0,
                style={
                    'width': '100%',
                    'padding': '10px',
                    'backgroundColor': '#2c8cff',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '4px',
                    'cursor': 'pointer',
                    'fontSize': '13px',
                    'fontWeight': 'bold',
                    'marginBottom': '10px'
                }
            ),
            
            # Contenitore per i controlli di selezione
            html.Div(
                id="compare-controls",
                style={'display': 'none'},
                children=[
                    html.Label(
                        "Select Countries to Compare:",
                        style={'fontWeight': 'bold', 'fontSize': '13px', 'marginTop': '10px', 'display': 'block'}
                    ),
                    html.Div(
                        "Click countries on the map or use the dropdown below",
                        style={'fontSize': '11px', 'color': '#666', 'marginBottom': '10px', 'fontStyle': 'italic'}
                    ),
                    
                    # Dropdown per selezionare i paesi
                    dcc.Dropdown(
                        id="compare-dropdown",
                        options=[],
                        value=[],
                        multi=True,
                        placeholder="Select countries...",
                        style={'marginBottom': '10px', 'fontSize': '12px'}
                    ),
                    
                    # Bottoni per azioni
                    html.Div(
                        style={'display': 'flex', 'gap': '8px', 'marginBottom': '10px'},
                        children=[
                            html.Button(
                                "Clear Selection",
                                id="clear-compare-btn",
                                n_clicks=0,
                                style={
                                    'flex': '1',
                                    'padding': '8px',
                                    'backgroundColor': '#dc3545',
                                    'color': 'white',
                                    'border': 'none',
                                    'borderRadius': '4px',
                                    'cursor': 'pointer',
                                    'fontSize': '12px'
                                }
                            ),
                            
                        ]
                    ),
                    
                    # Container per il parallel plot
                    html.Div(
                        id="parallel-container",
                        style={'display': 'none', 'marginTop': '10px'},
                        children=[
                            dcc.Graph(
                                id="parallel-plot",
                                config={"displayModeBar": False},
                                style={"height": "300px"}
                            )
                        ]
                    )
                ]
            )
        ]
    )


def generate_info_tooltip():
    """
    Backdrop (Sfondo click-away) e Scheda Informativa.
    """
    backdrop_style = {
        'position': 'fixed',
        'top': '-100vh',
        'left': '-100vw',
        'width': '300vw',
        'height': '300vh',
        'zIndex': 2998,
        'display': 'none',
        'cursor': 'default',
        'backgroundColor': 'transparent'
    }

    card_style = {
        'position': 'absolute',
        'top': '35px',
        'right': '0px',
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
        'display': 'none'
    }

    return html.Div([
        html.Div(id="info-backdrop", style=backdrop_style, n_clicks=0),
        html.Div(
            style={
                'position': 'absolute',
                'top': '15px',
                'right': '15px',
                'zIndex': 3000
            },
            children=[
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

                        html.Div("Click anywhere else to close",
                                 style={'fontSize': '10px', 'color': '#aaa', 'marginTop': '10px', 'textAlign': 'right',
                                        'fontStyle': 'italic'})
                    ]
                )
            ]
        )
    ])


def make_menu_layout(include_compare=True):
    children = [
        generate_info_tooltip(),
        generate_description_card(),
        html.Hr(style={'margin': '15px 0'}),
        generate_control_card(),
    ]

    if include_compare:
        children.append(generate_compare_controls())

    return html.Div(
        id="floating-menu",
        children=children,
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
            'overflow': 'auto'
        }
    )
