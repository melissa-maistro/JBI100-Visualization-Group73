from dash import dcc, html
import plotly.graph_objects as go


class Scatterplot(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        # Create initial figure with improved styling
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df[self.feature_x],
            y=self.df[self.feature_y],
            mode='markers',
            marker=dict(
                size=6,
                color='rgba(100, 149, 237, 0.6)',  # Cornflower blue with transparency
                line=dict(width=0.5, color='rgba(255, 255, 255, 0.8)')
            ),
            hovertemplate='<b>%{text}</b><br>' +
                         f'{self.feature_x}: %{{x:.3f}}<br>' +
                         f'{self.feature_y}: %{{y:.3f}}<extra></extra>',
            text=self.df['Country'] if 'Country' in self.df.columns else None
        ))
        
        fig.update_layout(
            xaxis_title=self.feature_x,
            yaxis_title=self.feature_y,
            yaxis_zeroline=True,
            xaxis_zeroline=True,
            plot_bgcolor='rgba(250, 250, 252, 1)',
            paper_bgcolor='white',
            font=dict(family="Arial, sans-serif", size=12, color="#555"),
            xaxis=dict(
                gridcolor='rgba(200, 200, 200, 0.3)',
                zerolinecolor='rgba(150, 150, 150, 0.5)',
                zerolinewidth=1
            ),
            yaxis=dict(
                gridcolor='rgba(200, 200, 200, 0.3)',
                zerolinecolor='rgba(150, 150, 150, 0.5)',
                zerolinewidth=1
            ),
            margin=dict(l=50, r=20, t=10, b=50),
            hovermode='closest'
        )

        super().__init__(
            className="graph_card",
            children=[dcc.Graph(id=self.html_id, figure=fig)]
        )

    def update(self, selected_color, selected_data):
        self.fig = go.Figure()

        x_values = self.df[self.feature_x]
        y_values = self.df[self.feature_y]
        
        # Add scatter trace with improved styling
        self.fig.add_trace(go.Scatter(
            x=x_values, 
            y=y_values,
            mode='markers',
            marker=dict(
                size=6,
                color='rgba(100, 149, 237, 0.6)',
                line=dict(width=0.5, color='rgba(255, 255, 255, 0.8)')
            ),
            hovertemplate='<b>%{text}</b><br>' +
                         f'{self.feature_x}: %{{x:.3f}}<br>' +
                         f'{self.feature_y}: %{{y:.3f}}<extra></extra>',
            text=self.df['Country'] if 'Country' in self.df.columns else None
        ))
        
        self.fig.update_layout(
            yaxis_zeroline=True,
            xaxis_zeroline=True,
            dragmode='select',
            plot_bgcolor='rgba(250, 250, 252, 1)',
            paper_bgcolor='white',
            font=dict(family="Arial, sans-serif", size=12, color="#555"),
            xaxis=dict(
                title=self.feature_x,
                gridcolor='rgba(200, 200, 200, 0.3)',
                zerolinecolor='rgba(150, 150, 150, 0.5)',
                zerolinewidth=1
            ),
            yaxis=dict(
                title=self.feature_y,
                gridcolor='rgba(200, 200, 200, 0.3)',
                zerolinecolor='rgba(150, 150, 150, 0.5)',
                zerolinewidth=1
            ),
            margin=dict(l=50, r=20, t=10, b=50),
            hovermode='closest'
        )
        
        self.fig.update_xaxes(fixedrange=True)
        self.fig.update_yaxes(fixedrange=True)

        # Highlight selected points
        if selected_data is None:
            selected_index = self.df.index
        elif isinstance(selected_data, list):
            selected_index = selected_data
        else:
            selected_index = [
                x.get('pointIndex', None)
                for x in selected_data.get('points', [])
            ]

        self.fig.data[0].update(
            selectedpoints=selected_index,
            selected=dict(
                marker=dict(
                    color=selected_color,
                    size=8,
                    opacity=1.0
                )
            ),
            unselected=dict(
                marker=dict(
                    color='rgba(100, 149, 237, 0.3)',
                    size=6,
                    opacity=0.4
                )
            )
        )

        return self.fig
