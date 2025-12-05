from dash import dcc, html
import plotly.graph_objects as go

class RadarView(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.risk_cols = ['Economic Risk', 'Demographic Risk', 'Infrastructure Risk', 'Social Risk']

        super().__init__(
            className="radar_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, selected_country):
        if not selected_country:
            # Media Globale se nessun paese selezionato
            values = self.df[self.risk_cols].mean().tolist()
            title = "Global Average Risk"
        else:
            country_data = self.df[self.df['Country'] == selected_country]
            if country_data.empty:
                return go.Figure()
            values = country_data[self.risk_cols].values.flatten().tolist()
            title = f"Risk Profile: {selected_country}"

        # Chiudiamo il cerchio del radar
        values += [values[0]]
        categories = self.risk_cols + [self.risk_cols[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=title
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1])
            ),
            showlegend=False,
            title=title,
            margin={"r":40,"t":40,"l":40,"b":40}
        )
        return fig