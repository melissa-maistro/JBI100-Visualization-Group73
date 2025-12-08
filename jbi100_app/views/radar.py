from dash import dcc, html
import plotly.graph_objects as go

class RadarView(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        # I nomi delle colonne nel CSV processato
        self.risk_cols = ['Economic Risk', 'Social Risk', 'Infrastructure Risk', 'Demographic Risk']

        super().__init__(
            className="radar_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, selected_country):
        fig = go.Figure()

        # Logica: Se non c'è paese selezionato, mostra la media globale
        if not selected_country:
            # Calcola media solo sulle colonne numeriche
            avg_values = self.df[self.risk_cols].mean().tolist()
            # Chiudi il cerchio
            avg_values += [avg_values[0]]
            plot_values = avg_values
            title = "Global Average Risk Profile"
            line_color = 'blue'
        else:
            # Filtra il paese
            country_data = self.df[self.df['Country'] == selected_country]
            
            # Se il paese non esiste nel CSV (es. clicchi sull'oceano o su un'area grigia)
            if country_data.empty:
                return go.Figure().update_layout(title=f"No data for {selected_country}")

            values = country_data[self.risk_cols].values.flatten().tolist()
            values += [values[0]]
            plot_values = values
            title = f"Risk Profile: {selected_country}"
            line_color = 'red'

        categories = self.risk_cols + [self.risk_cols[0]]

        fig.add_trace(go.Scatterpolar(
            r=plot_values,
            theta=categories,
            fill='toself',
            name=title,
            line_color=line_color
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1] # Importante: Fissa la scala max a 1
                )
            ),
            showlegend=False,
            title=dict(text=title, x=0.5),
            margin={"r":40,"t":40,"l":40,"b":40}
        )
        return fig