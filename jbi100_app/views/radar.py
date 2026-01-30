from dash import dcc, html
import plotly.graph_objects as go


class RadarView(html.Div):
    """
    Displays detailed risk profile for a single country (or global average)
    using a Radar (Spider) Chart.
    """
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Define the axes of the radar chart
        self.risk_cols = [
            'Economic Risk',
            'Demographic Risk',
            'Infrastructure Risk',
            'Social Risk',
            'Transport Constraint',
        ]

        super().__init__(
            className="radar_card",
            children=[
                dcc.Graph(
                    id=self.html_id,
                    config={
                        'displayModeBar': False,
                        'scrollZoom': False,
                        'staticPlot': False
                    },
                    style={'height': '100%', 'width': '100%'}
                )
            ],
        )

    def update(self, selected_country, selected_risk=None):
        fig = go.Figure()

        # Shorten labels for better readability on the chart
        short_labels = {
            'Economic Risk': 'Economic',
            'Social Risk': 'Social',
            'Infrastructure Risk': 'Infrastr.',
            'Demographic Risk': 'Demographic',
            'Transport Constraint': 'Transport'
        }

        # Close the loop for the radar chart (repeat first category)
        display_categories = [short_labels.get(col, col) for col in self.risk_cols]
        display_categories += [display_categories[0]]

        # --- A. Data Preparation ---
        if not selected_country:
            # Fallback: Show Global Average if no country selected
            avg_values = self.df[self.risk_cols].mean().tolist()
            avg_values += [avg_values[0]] # Close loop
            plot_values = avg_values
            title_text = "Global Average"
            line_color = '#1E88E5'
            fill_color = 'rgba(30, 136, 229, 0.2)'
        else:
            # Specific Country Data
            country_data = self.df[self.df['Country'] == selected_country]
            if country_data.empty:
                return go.Figure().update_layout(title=dict(text="No data", x=0.5))

            values = country_data[self.risk_cols].values.flatten().tolist()
            values += [values[0]] # Close loop
            plot_values = values
            title_text = f"<b>{selected_country}</b>"
            line_color = '#D32F2F'
            fill_color = 'rgba(211, 47, 47, 0.2)'

        # Add subtitle if a specific risk metric is currently selected on the map
        if selected_risk:
            title_text += f"<br><span style='font-size:11px; color:grey; font-weight:normal'>Focus: {selected_risk}</span>"

        # --- B. Draw Trace ---
        fig.add_trace(go.Scatterpolar(
            r=plot_values,
            theta=display_categories,
            fill='toself',
            fillcolor=fill_color,
            name=selected_country if selected_country else "Global",
            line=dict(color=line_color, width=2),
            hoverinfo='r+theta'
        ))

        # --- C. Layout Configuration ---
        fig.update_layout(
            dragmode=False,
            polar=dict(
                gridshape='circular',  # Force circular grid instead of polygon

                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    gridcolor='#eee',
                    linecolor='#eee',
                    tickfont=dict(size=8, color='#999'),
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, color='#333', weight='bold'),
                    rotation=90,
                    ticklen=30,
                    tickcolor='white',
                    showline=True,   # Shows the outer boundary circle
                    linecolor='#eee',
                    linewidth=1
                ),
                bgcolor='white'
            ),
            showlegend=False,
            title=dict(
                text=title_text,
                x=0.5, y=0.90,
                xanchor='center', yanchor='top',
                font=dict(size=18, color='#2c3e50')
            ),
            margin={"t": 120, "l": 80, "r": 80, "b": 50},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig
