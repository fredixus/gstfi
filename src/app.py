'''
 # @ Create Time: 2024-05-15 10:46:18.134470
'''

import pathlib
from tkinter import Button
from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import plotly.express as px
import pandas as pd
import json, os

import linear

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

def load_json(path_and_filename):
    with open(path_and_filename) as f:
        return json.load(f)

def compose_main_guage_panel(df, columns, linear_output):
    """
    daq.Gauge(
        showCurrentValue=True,
        units="PLN",
        value=5,
        label='Default',
        max=10,
        min=0
    )
    """

    elements = []

    for column in columns:
        print(column)

        current_max =       round(float(df.tail(1)[column].values[0]),2)
        current_min =       round(float(df.min()[column]),2)
        curren_label =      column
        current_value =     round(float(linear_output[column]),2)

        elements.append(
            daq.Gauge(
                showCurrentValue=True,
                units="PLN",
                value=current_value,
                label=curren_label,
                max=current_max,
                min=current_min
            )
        )

    return html.Div(elements)

df = load_data("data.csv")
columns = list(df.columns)
columns = [{'label': name, 'value':name} for name in columns][2:]
current_columns = []

current_folder = os.path.join(os.getcwd(),'src/data')
series_names = load_json(os.path.join(current_folder, "names.json"))

defaultSeries = series_names[0] # 'Goldman Sachs Japonia (K)'

series_names = [{'label': name, 'value':name} for name in series_names]



app.layout = html.Div([
    html.H4('Select stock field'),
    dcc.Dropdown(id ='field_picker', options = series_names, value = defaultSeries, searchable = True, multi = False),
    daq.BooleanSwitch(id='field_picker_switch', on=True),

    html.H5('Select graph series'),
    dcc.Dropdown(id ='column_picker', options = columns, value = defaultSeries, searchable = True, multi = True),
    dcc.Graph(id = "graph"),

    html.Button('Get predictions', id = 'get_linear_predictions'),
    html.Div(id='temp_output_predictions'),

    html.Div(id='main_guage_panel'),
    
])

@app.callback(
    Output('column_picker', 'options'),
    Input('field_picker_switch', 'on'),
    Input('field_picker', 'value'),
    
)
def update_column_picker_options(on, value):
    value = value[:value.find(" (")]

    if on:
        return [column for column in columns if (column['value'].find(value) == 0)]
    else:
        return columns

@app.callback(
    Output("temp_output_predictions", "children"),
    Output("main_guage_panel", "children"),
    Input('field_picker_switch', 'on'),
    Input('field_picker', 'value'),
    Input("get_linear_predictions", "n_clicks"))
def update_predictions(on, value, n_clicks):
    linear_output = linear.get_linear_predictions(future_days = 30)
    print("Updated")

    if on:
        value = value[:value.find(" (")]
        current_columns = [column for column in columns if (column['value'].find(value) == 0)]
        guage_panel = compose_main_guage_panel(df, [ value['value']  for value in current_columns], linear_output)
    else:
        guage_panel = compose_main_guage_panel(df, [ value['value']  for value in columns], linear_output)
    
    return None, guage_panel

@app.callback(
    Output("graph", "figure"),
    Input("column_picker", "value"))
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
