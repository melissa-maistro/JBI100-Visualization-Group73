from dash import dcc, html
import plotly.graph_objects as go


class TransportRankView(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(
                    id=self.html_id,
                    config={"displayModeBar": False},
                    style={"height": "100%", "width": "100%"}
                )
            ],
        )

    def update(self, top_n=15, selected_countries=None):
        if selected_countries is None:
            selected_countries = []

        if "Transport Constraint" not in self.df.columns:
            return go.Figure()

        plot_df = self.df[["Country", "Transport Constraint"]].dropna()
        plot_df = plot_df.sort_values("Transport Constraint", ascending=False).head(top_n)

        colors = [
            "#1E88E5" if c in selected_countries else "#E57373"
            for c in plot_df["Country"]
        ]
        y_vals = plot_df["Country"].tolist()

        fig = go.Figure(
            data=[
                go.Bar(
                    x=plot_df["Transport Constraint"],
                    y=plot_df["Country"],
                    orientation="h",
                    marker=dict(color=colors, line=dict(color="white", width=0.5)),
                    hovertemplate="<b>%{y}</b><br>Constraint: %{x:.2f}<extra></extra>",
                )
            ]
        )

        fig.update_layout(
            title=dict(
                text="Transport Constraint — Highest Priority",
                x=0.5,
                font=dict(size=14, color="#2c3e50")
            ),
            xaxis=dict(
                title="Constraint Index (higher = worse)",
                range=[0, 1],
                gridcolor="rgba(200, 200, 200, 0.3)"
            ),
            yaxis=dict(
                autorange="reversed",
                categoryorder="array",
                categoryarray=y_vals,
                tickmode="array",
                tickvals=y_vals,
                ticktext=y_vals,
                tickfont=dict(size=11),
                automargin=True
            ),
            margin=dict(l=80, r=20, t=40, b=40),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )

        return fig
