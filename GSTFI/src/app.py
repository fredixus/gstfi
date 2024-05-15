'''
 # @ Create Time: 2024-05-15 10:46:18.134470
'''

import pathlib
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__, title="GSTFI")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

def load_data(data_file: str) -> pd.DataFrame:
    '''
    Load data from /data directory
    '''
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    return pd.read_csv(DATA_PATH.joinpath(data_file))

df = load_data("data.csv")
columns = list(df.columns)
columns = [{'label': name, 'value':name} for name in columns][2:]
defaultSeries = 'Goldman Sachs Japonia (K)'

app.layout = html.Div([
    html.H4('Simple stock plot with adjustable axis'),
    dcc.Dropdown(id ='columnPicker', options = columns, value = defaultSeries, searchable = True, multi = True),
    dcc.Graph(id = "graph"),

    
])

"""@app.callback(
    Output("columnPicker", "figure"),
    Input("button", "n_clicks"))
def display_graph(n_clicks):
    # replace with your own data source
    

    if n_clicks % 2 == 0:
        x, y = 'Data', 'AAPL_y'
    else:
        x, y = 'AAPL_y', 'Data'

    fig = px.line(df, x=x, y=y)
    return fig"""

@app.callback(
    Output("graph", "figure"),
    Input("columnPicker", "value"))
def update_graph(value):
    # replace with your own data source

    if (isinstance(value, list)):
        if(len(value) > 0):
            dff = df[['Data', *value]]
        else:
            dff = df[['Data', defaultSeries]]
    else:
       dff = df[['Data', value]]

    col = list(dff.columns)
    return px.line(dff, x=col[0], y=col[1:])


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
