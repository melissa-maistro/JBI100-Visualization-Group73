from dash import dcc, html
import plotly.graph_objects as go
import plotly.colors as pc


class CompareView(html.Div):
    """
    Comparison View: Displays a parallel-coordinates style plot
    comparing risk metrics across selected countries.
    """

    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.risk_cols = [
            "Economic Risk",
            "Social Risk",
            "Infrastructure Risk",
            "Demographic Risk",
            "Transport Constraint",
        ]

        super().__init__(
            className="compare_card",
            children=[
                dcc.Graph(
                    id=self.html_id,
                    config={"displayModeBar": False, "scrollZoom": False},
                    style={"height": "100%", "width": "100%"}
                )
            ],
        )

    def update(self, selected_countries):
        fig = go.Figure()

        # Handle empty selection case
        if not selected_countries:
            fig.update_layout(
                title="Select countries to compare",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis={'visible': False}, yaxis={'visible': False}
            )
            return fig

        # 1. Add Global Mean (Baseline Reference)
        global_mean = self.df[self.risk_cols].mean().tolist()
        fig.add_trace(go.Scatter(
            x=self.risk_cols,
            y=global_mean,
            mode="lines",
            name="Global Mean",
            line=dict(color="gray", dash="dot", width=2),
            opacity=0.5
        ))

        # 2. Add Traces for Selected Countries
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
                # Cycle through color palette
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8)
            ))

        # 3. Layout Configuration
        fig.update_layout(
            title=dict(text="Risk Comparison (Parallel Plot)", x=0.5, font=dict(size=14)),
            yaxis=dict(range=[0, 1.05], title="Risk Score", gridcolor='#eee', fixedrange=True),
            xaxis=dict(showgrid=True, gridcolor='#eee', fixedrange=True),
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
            margin=dict(l=40, r=20, t=60, b=40),
            paper_bgcolor='white',
            plot_bgcolor='white',
            hovermode="x unified"  # Shows all values for a metric on hover
        )
        return fig