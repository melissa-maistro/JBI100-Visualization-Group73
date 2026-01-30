from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go


class MapView(html.Div):
    """
    Main component for the Choropleth Map.
    Renders the geographical risk distribution and handles highlighting logic.
    """
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Initialize as a full-screen fixed container
        super().__init__(
            className="map_card",
            style={
                'top': '0', 'left': '0',
                'width': '100vw', 'height': '100vh',
                'margin': '0', 'padding': '0',
                'position': 'fixed', 'zIndex': '1'
            },
            children=[
                dcc.Graph(
                    id=self.html_id,
                    style={'height': '100vh', 'width': '100%', 'display': 'block'},
                    config={
                        'displayModeBar': True,
                        'displaylogo': False,
                        # Remove unnecessary buttons to keep UI clean
                        'modeBarButtonsToRemove': [
                            'select2d', 'lasso2d', 'autoScale2d',
                            'resetScale2d', 'hoverClosestGeo',
                            'hoverCompareCartesian', 'toggleSpikelines',
                            'toImage', 'resetGeo'
                        ],
                        'scrollZoom': True
                    }
                )
            ],
        )

    def update(self, selected_risk, highlight_countries=None, colorblind_mode=False):
        """
        Updates the map figure based on the selected risk variable.
        Args:
            selected_risk (str): The column name to visualize.
            highlight_countries (list): List of country names to highlight with a border.
            colorblind_mode (bool): Switches color palette if True.
        """
        if selected_risk not in self.df.columns:
            return {}

        # 1. Select Color Scale based on accessibility mode
        colorscale = "Viridis" if colorblind_mode else "RdYlGn_r"

        # 2. Base Choropleth Layer (All Countries)
        fig = px.choropleth(
            self.df,
            locations="Country",
            locationmode='country names',
            color=selected_risk,
            hover_name="Country",
            hover_data={'Country': False},
            color_continuous_scale=colorscale,
            range_color=[0, 1],
            projection="natural earth"
        )

        # Style the base polygons
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=1,
            marker_opacity=0.85
        )

        # 3. Highlight Layer (Overlay)
        # Draws a secondary trace for selected countries with a cyan border
        if highlight_countries:
            highlight_df = self.df[self.df['Country'].isin(highlight_countries)]
            if not highlight_df.empty:
                fig.add_trace(go.Choropleth(
                    locations=highlight_df['Country'],
                    locationmode='country names',
                    z=highlight_df[selected_risk],
                    colorscale=colorscale,
                    zmin=0, zmax=1,
                    showscale=False,
                    # Thick cyan line for visibility
                    marker=dict(line=dict(color='cyan', width=3), opacity=1),
                    hoverinfo='skip'
                ))

        # 4. Final Layout Adjustments
        fig.update_layout(
            dragmode="pan",
            uirevision=selected_risk,  # Preserves zoom state on update
            margin=dict(l=0, r=0, t=50, b=0, pad=0, autoexpand=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='natural earth',
                projection_scale=1.05
            ),
            # Custom position for the legend/colorbar
            coloraxis_colorbar=dict(
                title="Risk Level",
                x=0.11, y=0.5,
                len=0.4, thickness=15
            )
        )

        return fig