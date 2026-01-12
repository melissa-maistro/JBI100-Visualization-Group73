from dash import dcc, html
import plotly.graph_objects as go

class CompareView(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # colonne dei rischi nel CSV processato
        self.risk_cols = [
            "Economic Risk",
            "Social Risk",
            "Infrastructure Risk",
            "Demographic Risk",
        ]

        super().__init__(
            className="compare_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, selected_countries, selected_dims=None):
        """
        selected_countries: list[str]
        selected_dims: list[str] of risk columns
        """
        if selected_dims is None or len(selected_dims) == 0:
            selected_dims = self.risk_cols

        fig = go.Figure()

        # Reference: global mean (baseline)
        global_mean = self.df[selected_dims].mean().tolist()
        fig.add_trace(
            go.Scatter(
                x=selected_dims,
                y=global_mean,
                mode="lines+markers",
                name="Global mean",
                line=dict(dash="dash"),
            )
        )

        # Se nessun paese selezionato, mostra solo baseline
        if not selected_countries:
            fig.update_layout(
                title=dict(text="Compare Countries: select countries to start", x=0.5),
                yaxis=dict(range=[0, 1], title="Risk (0–1)"),
                xaxis=dict(title="Risk dimension"),
                margin=dict(l=40, r=20, t=50, b=40),
            )
            return fig

        # Tracce per ciascun paese
        for country in selected_countries:
            row = self.df[self.df["Country"] == country]
            if row.empty:
                continue

            vals = row[selected_dims].values.flatten().tolist()

            fig.add_trace(
                go.Scatter(
                    x=selected_dims,
                    y=vals,
                    mode="lines+markers",
                    name=country,
                )
            )

        fig.update_layout(
            title=dict(text="Compare Countries Across Risk Dimensions", x=0.5),
            yaxis=dict(range=[0, 1], title="Risk (0–1)"),
            xaxis=dict(title="Risk dimension"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            margin=dict(l=40, r=20, t=70, b=40),
        )
        return fig