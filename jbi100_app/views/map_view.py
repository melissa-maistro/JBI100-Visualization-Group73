from dash import dcc, html
import plotly.express as px


class MapView(html.Div):
    def __init__(self, name, df, default_risk="Total Vulnerability"):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        super().__init__(
            className="map_card",
            style={
                "top": "0",
                "left": "0",
                "width": "100vw",
                "height": "100vh",
                "margin": "0",
                "padding": "0",
                "position": "fixed",
                "zIndex": "1",
            },
            children=[
                dcc.Graph(
                    id=self.html_id,
                    style={"height": "100vh", "width": "100%", "display": "block"},
                    config={"displayModeBar": False, "scrollZoom": True},
                    figure=self.update(default_risk, []),
                )
            ],
        )

    def update(self, selected_risk, compare_countries=None):
        if compare_countries is None:
            compare_countries = []

        if not selected_risk:
            selected_risk = "Total Vulnerability"

        plot_df = self.df.copy()
        plot_df["border_width"] = plot_df["Country"].apply(
            lambda x: 3 if x in compare_countries else 0.5
        )
        plot_df["border_color"] = plot_df["Country"].apply(
            lambda x: "black" if x in compare_countries else "white"
        )

        fig = px.choropleth(
            plot_df,
            locations="Country",
            locationmode="country names",
            color=selected_risk,
            hover_name="Country",
            color_continuous_scale="RdYlGn_r",
            range_color=[0, 1],
            projection="natural earth",
        )

        fig.update_traces(
            marker_line_color=plot_df["border_color"],
            marker_line_width=plot_df["border_width"],
            marker_opacity=0.9,
        )

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type="natural earth",
                bgcolor="rgba(0,0,0,0)",
            ),
            coloraxis_colorbar=dict(
                x=0.02,
                y=0.5,
                len=0.4,
                title="Risk Level",
                bgcolor="rgba(255,255,255,0.6)",
                thickness=15,
            ),
        )
        return fig
