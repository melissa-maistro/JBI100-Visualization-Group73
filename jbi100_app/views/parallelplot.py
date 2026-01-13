from dash import dcc, html
import plotly.graph_objects as go


class ParallelPlotView(html.Div):
    """
    Parallel coordinates plot for comparing selected countries on risk dimensions.
    """

    def __init__(self, name: str, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Colonne attese (coerenti col vostro progetto)
        self.dim_cols = [
            "Economic Risk",
            "Social Risk",
            "Infrastructure Risk",
            "Demographic Risk",
        ]

        super().__init__(
            children=[
                dcc.Graph(
                    id=self.html_id,
                    config={"displayModeBar": False},
                    style={"height": "520px"},
                    figure=go.Figure()
                )
            ]
        )

    def update(self, selected_countries):
        fig = go.Figure()

        if not selected_countries:
            fig.update_layout(
                title="Parallel Plot (select countries to compare)",
                margin=dict(l=30, r=30, t=50, b=30),
            )
            return fig

        df_sel = self.df[self.df["Country"].isin(selected_countries)].copy()
        if df_sel.empty:
            fig.update_layout(
                title="Parallel Plot (no data for selected countries)",
                margin=dict(l=30, r=30, t=50, b=30),
            )
            return fig

        # Garantisci che le colonne siano numeriche
        for c in self.dim_cols:
            df_sel[c] = df_sel[c].astype(float)

        # Costruzione dimensioni
        dimensions = []
        for c in self.dim_cols:
            dimensions.append(
                dict(
                    label=c,
                    values=df_sel[c].values,
                    range=[0, 1]
                )
            )

        # Parallel Coordinates
        fig.add_trace(
            go.Parcoords(
                line=dict(
                    color=list(range(len(df_sel))),
                    showscale=False,
                ),
                dimensions=dimensions,
                # Mostriamo i nomi in hover via customdata
                customdata=df_sel["Country"].tolist(),
                hoveron="lines",
                hovertemplate="Country: %{customdata}<extra></extra>",
            )
        )

        fig.update_layout(
            title="Parallel Plot Comparison",
            margin=dict(l=30, r=30, t=60, b=30),
            paper_bgcolor="white",
            plot_bgcolor="white",
        )

        return fig