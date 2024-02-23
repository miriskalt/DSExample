import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px



app = dash.Dash(__name__)
server = app.server

### Import data

df = pd.read_csv('./data/Takeout/Fitbit/')
df = df[[' Matrikel_nr', ' Hauptfach', ' Fachsemester']]


### App layout

app.layout = html.Div([
    html.H1("This is a sample project using human data", style={'text-align': 'center'}),
    html.P('The following interactive linegraph visualizes the selected features over the entire timespan of the dataset'),


    dcc.Dropdown(id="feature_selection",
                 options=[
                     {'label': "Deep Sleep in Minutes", 'value': 'deep_sleep_in_minutes'},
                     {'label': "Overall Score", 'value': 'overall_score'},
                     {'label': "Resting Heart Rate", 'value': 'resting_heart_rate'}],
                 multi=False,
                 value='overall_score', # init value
                 style={'width': '40%'}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(), # whitespace

    dcc.Graph(id='first_graph', figure={})

    ]
)

### Callbacks
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='first_graph', component_property='figure')],
     [Input(component_id='feature_selection', component_property='value')]
)
def update_graph(option_selection):
    print(option_selection)
    print(type(option_selection))

    container = "The plot shows: {}".format(option_selection)

    # update the data 
    dff = df.copy()
    print('copied')
    dff = dff[option_selection]
    # dff = dff[dff[' Hauptfach'] == option_selection]
    # print('filtered', dff.shape)
    # create graph
    fig = px.scatter(
        data_frame = dff,
        x = 'timestamp',
        y = option_selection.get,
    )
    return container, fig



print("Ran through.")


if __name__ == '__main__':
   app.run_server(debug=True)