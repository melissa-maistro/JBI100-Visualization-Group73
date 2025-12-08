from dash import dcc, html
import plotly.express as px

class MapView(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        
        super().__init__(
            className="map_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, selected_risk):
        # Definiamo una scala colore semantica
        # RdYlGn_r: Verde (Basso) -> Giallo -> Rosso (Alto)
        
        fig = px.choropleth(
            self.df,
            locations="Country",
            locationmode='country names',
            color=selected_risk,
            hover_name="Country",
            color_continuous_scale="RdYlGn_r", 
            range_color=[0, 1], # Fissa la scala da 0 a 1 per coerenza
            title=f"Global View: {selected_risk}",
            projection="natural earth" # O 'orthographic' per il mappamondo 3D
        )
        
        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            coloraxis_colorbar=dict(title="Risk Level")
        )
        
        # Abilita lo zoom e il pan nativi di Plotly
        return fig