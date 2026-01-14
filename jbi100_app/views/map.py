from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go


class MapView(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        super().__init__(
            className="map_card",
            style={
                'top': '0',
                'left': '0',
                'width': '100vw',
                'height': '100vh',
                'margin': '0',
                'padding': '0',
                'position': 'fixed',
                'zIndex': '1'
            },
            children=[
                dcc.Graph(
                    id=self.html_id,
                    style={'height': '100vh', 'width': '100%', 'display': 'block'},
                    config={'displayModeBar': False, 'scrollZoom': True}
                )
            ],
        )

    def update(self, selected_risk, brushed_countries=None):
        """
        Update map with selected risk variable and highlight brushed countries
        
        Args:
            selected_risk: The risk variable to display
            brushed_countries: List of country names to highlight in red (from PCA brushing)
        """
        if brushed_countries is None:
            brushed_countries = []
        
        # Verify the selected risk exists in the dataframe
        if selected_risk not in self.df.columns:
            return {}

        # Create base choropleth with risk data
        fig = px.choropleth(
            self.df,
            locations="Country",
            locationmode='country names',
            color=selected_risk,
            hover_name="Country",
            hover_data={'Country': False},
            color_continuous_scale="RdYlGn_r",
            range_color=[0, 1],
            projection="natural earth"
        )

        # Update base trace styling
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=1,
            marker_opacity=0.85
        )

        # Add elegant overlay for brushed countries
        if brushed_countries:
            brushed_df = self.df[self.df['Country'].isin(brushed_countries)]
            
            # Create a pulsing effect with a vibrant accent color
            fig.add_trace(go.Choropleth(
                locations=brushed_df['Country'],
                locationmode='country names',
                z=[1] * len(brushed_df),  # Dummy values for uniform color
                colorscale=[[0, 'rgba(100, 149, 237, 0.5)'], [1, 'rgba(100, 149, 237, 0.5)']],  # Cornflower blue
                showscale=False,
                marker_line_color='rgba(65, 105, 225, 1)',  # Royal blue border
                marker_line_width=3,
                marker_opacity=0.65,
                hovertemplate='<b>%{location}</b><br><i>Selected from PCA</i><extra></extra>',
                name='Selected Countries'
            ))

        # Update layout
        fig.update_layout(
            dragmode=False,
            margin=dict(l=0, r=0, t=0, b=0, pad=0, autoexpand=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='natural earth',
                projection_scale=1.05,
                center=dict(lat=0, lon=0)
            ),
            title=dict(
                text=f"Global Risk Map: {selected_risk}",
                y=0.95,
                x=0.5,
                xanchor='center',
                yanchor='top',
                automargin=False,
                pad=dict(t=10)
            ),
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