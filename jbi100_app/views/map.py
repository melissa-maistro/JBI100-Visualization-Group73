from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

# 2. La tua Classe MapView (Ottimizzata per interattività Client-Side)
class MapView(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        super().__init__(
            className="map_card",
            # Stile container: Definisce i limiti fisici della mappa nella pagina
            style={
                'top': '0',
                'left': '0',
                'width': '100vw',
                'height': '100vh',  # L'altezza si adatta al contenuto
                'margin': '0',
                'padding': '0',
                'position': 'fixed',  # Necessario per gestire le sovrapposizioni
                'zIndex': '1'  # Assicura un livello di base coerente
            },
            children=[
                dcc.Graph(
                    id=self.html_id,
                    style={'height': '100vh', 'width': '100%', 'display': 'block'},
                    config={
                        # 1. Attiva la barra dei comandi
                        'displayModeBar': True,

                        # 2. Nascondi il logo di Plotly
                        'displaylogo': False,

                        # 3. Rimuovi tutti i tasti inutili, tieni solo Zoom (+/-) e Pan
                        'modeBarButtonsToRemove': [
                            'select2d', 'lasso2d', 'autoScale2d',
                            'resetScale2d', 'hoverClosestGeo',
                            'hoverCompareCartesian', 'toggleSpikelines',
                            'toImage', 'resetGeo'
                        ],

                        # 4. Abilita lo zoom con la rotellina del mouse
                        'scrollZoom': True
                    }
                )
            ],
        )

    def update(self, selected_risk, highlight_countries=None):
            # Verifica se il rischio selezionato esiste
            if selected_risk not in self.df.columns:
                return {}

            # Mappa Base
            fig = px.choropleth(
                self.df,
                locations="Country",
                locationmode='country names',
                color=selected_risk,
                hover_name="Country",
                hover_data={'Country': False},
                color_continuous_scale="RdYlGn_r",
                range_color=[0, 1],
                projection="natural earth"
            )

            fig.update_traces(
                marker_line_color='white',
                marker_line_width=1,
                marker_opacity=0.85
            )

            # --- AGGIUNTA: EVIDENZIA PAESI SELEZIONATI ---
            if highlight_countries:
                # Filtra il dataframe per prendere solo i paesi selezionati
                highlight_df = self.df[self.df['Country'].isin(highlight_countries)]
                
                if not highlight_df.empty:
                    fig.add_trace(go.Choropleth(
                        locations=highlight_df['Country'],
                        locationmode='country names',
                        z=highlight_df[selected_risk], # Serve per mantenere il colore corretto
                        colorscale="RdYlGn_r",
                        zmin=0, zmax=1,
                        showscale=False, # Nascondi la seconda colorbar
                        marker=dict(
                            line=dict(color='cyan', width=3), # Bordo CYAN spesso
                            opacity=1
                        ),
                        hoverinfo='skip' # Non mostrare doppio tooltip
                    ))
            # ---------------------------------------------

            fig.update_layout(
                dragmode=False,
                margin=dict(l=0, r=0, t=0, b=0, pad=0, autoexpand=False),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='natural earth',
                    projection_scale=1.05,
                    center=dict(lat=0, lon=0)
                ),
                title=dict(
                    text=f"Global risk map: {selected_risk}",
                    y=0.95, x=0.86,
                    font=dict(family="Helvetica, Arial, sans-serif", size=20, color="#333"),
                    xanchor='center', yanchor='top',
                    automargin=False,
                    pad=dict(t=10)
                ),
                coloraxis_colorbar=dict(
                    title="Risk Level",
                    x=0.11, xanchor="center",
                    y=0.5, yanchor="middle",
                    len=0.4, thickness=15
                ),
                hoverlabel=dict(
                    bgcolor="rgba(255, 255, 255, 0.95)",
                    font_size=15,
                    bordercolor="#333",
                    namelength=-1
                )
            )

            return fig