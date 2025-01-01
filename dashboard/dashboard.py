from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

import os
from analysis import cuisine_top_ingredients, ingredient_top_cuisines, cuisine_uniqueness


# df = pd.read_csv(os.getenv('cuisines_analysis_final_csv'))
app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div(
                html.H1('Ingredients & Cuisines Dashboard'),
                className='title'
            )
        )
    ]      
    )
            ])

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)