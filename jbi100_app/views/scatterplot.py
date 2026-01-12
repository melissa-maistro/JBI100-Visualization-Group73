# jbi100_app/views/scatterplot.py

from dash import dcc, html
import plotly.graph_objects as go

class Scatterplot(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, selected_color, selected_data):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.df[self.feature_x],
            y=self.df[self.feature_y],
            mode='markers',
            marker=dict(
                size=10,
                color='rgba(0, 100, 200, 0.6)', # Colore base blu semi-trasparente
                line=dict(width=1, color='DarkSlateGrey')
            ),
            text=self.df['Country'], # Mostra nome paese al mouseover
            hoverinfo='text+x+y'
        ))

        fig.update_layout(
            title=f"{self.feature_x} vs {self.feature_y}",
            xaxis_title=self.feature_x,
            yaxis_title=self.feature_y,
            margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
            hovermode='closest',
            dragmode='select' # Abilita selezione box/lasso
        )

        return fig