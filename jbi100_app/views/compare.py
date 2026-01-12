from dash import dcc, html
import plotly.graph_objects as go
import plotly.colors as pc

class CompareView(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        self.risk_cols = [
            "Economic Risk",
            "Social Risk",
            "Infrastructure Risk",
            "Demographic Risk",
        ]

        super().__init__(
            className="compare_card",
            children=[
                dcc.Graph(id=self.html_id, config={"displayModeBar": False}, style={"height": "400px"})
            ],
        )

    def update(self, selected_countries):
        fig = go.Figure()
        
        # Gestione caso lista vuota
        if not selected_countries:
            return fig

        # Baseline: Media Globale
        global_mean = self.df[self.risk_cols].mean().tolist()
        fig.add_trace(go.Scatter(
            x=self.risk_cols,
            y=global_mean,
            mode="lines",
            name="Global Mean",
            line=dict(color="black", dash="dot", width=2),
            opacity=0.5
        ))

        # Colori per i paesi
        colors = pc.qualitative.Bold

        for i, country in enumerate(selected_countries):
            row = self.df[self.df["Country"] == country]
            if row.empty: continue

            vals = row[self.risk_cols].values.flatten().tolist()
            
            fig.add_trace(go.Scatter(
                x=self.risk_cols,
                y=vals,
                mode="lines+markers",
                name=country,
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8)
            ))

        fig.update_layout(
            title=dict(text="Risk Comparison", x=0.5),
            yaxis=dict(range=[0, 1.05], title="Risk Score", gridcolor='#eee'),
            xaxis=dict(showgrid=True, gridcolor='#eee'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=20, t=60, b=40),
            paper_bgcolor='white',
            plot_bgcolor='white',
            hovermode="x unified"
        )
        return fig