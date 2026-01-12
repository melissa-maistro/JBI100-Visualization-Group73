from dash import dcc, html
import plotly.express as px


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

    def update(self, selected_risk):
        # Verifica se il rischio selezionato esiste nel dataframe
        if selected_risk not in self.df.columns:
            return {}

        fig = px.choropleth(
            self.df,
            locations="Country",
            locationmode='country names',
            color=selected_risk,
            hover_name="Country",
            hover_data={'Country': False},
            color_continuous_scale="RdYlGn_r",
            range_color=[0, 1],
            # title=f"Global View: {selected_risk}",
            projection="natural earth"
        )

        # OTTIMIZZAZIONE VISIVA & INTERATTIVITÀ (Client-Side)
        # Non possiamo cambiare colore al volo senza JS custom, ma possiamo
        # giocare con l'opacità e i bordi per far risaltare la selezione.
        fig.update_traces(
            marker_line_color='white',  # Bordo bianco netto
            marker_line_width=1,  # Spessore bordo standard
            marker_opacity=0.85 # Opacità < 1 fa risaltare meglio il contenuto sotto il cursore
        )

        fig.update_layout(
            dragmode=False,

            # 1. MARGINI A ZERO (La mappa tocca i bordi fisici)
            margin=dict(l=0, r=0, t=0, b=0, pad=0, autoexpand=False),

            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='natural earth',
                # Se vuoi ridurre le bande bianche sopra/sotto dovute alla forma della terra:
                projection_scale=1.05,
                center=dict(lat=0, lon=0)
            ),

            # 2. TITOLO IN OVERLAY
            title=dict(
                text=f"Global risk map: {selected_risk}",
                # y=0.95 lo posiziona in alto, ma DENTRO l'area del grafico
                y=0.95,
                x=0.86,
                # --- QUI SI CAMBIA IL FONT ---
                font=dict(
                    family="Helvetica, Helvetica neue, Arial, sans-serif",  # Il font richiesto
                    size=20,  # Grandezza (puoi aumentarla se vuoi)
                    color="#333"  # Colore scuro (grigio scuro/nero)
                ),
                xanchor='center',
                yanchor='top',
                # FONDAMENTALE: automargin=False impedisce la creazione della barra bianca
                automargin=False,
                pad=dict(t=10)  # Un piccolo spazio dal bordo fisico del monitor per estetica
            ),

            # ... resto delle configurazioni (coloraxis, hoverlabel)...
            coloraxis_colorbar=dict(
                title="Risk Level",
                x=0.11, xanchor="center",
                y=0.5, yanchor="middle",
                len=0.4, thickness=15
            ),
            hoverlabel=dict(
                bgcolor="rgba(255, 255, 255, 0.95)",
                font_size=15,
                font_family="Arial",
                bordercolor="#333",
                namelength=-1
            )
        )

        return fig
