
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px



app = dash.Dash(__name__)

### Import data

df = pd.read_csv('../Teilnehmerliste.csv')
df = df[[' Matrikel_nr', ' Vorname', ' Hauptfach', ' Fachsemester']]


### App layout

app.layout = html.Div([
    html.H1("This is a heading", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_something",
                 options=[
                     {'label': "First Option", 'value': 79},
                     {'label': "Second Option", 'value': 277},
                     {'label': "Third Option", 'value': 128}],
                 multi=False,
                 value=227, # init value
                 style={'width': '40%'}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(), # whitespace

    dcc.Graph(id='a_graph', figure={})

    ]
)

### Callbacks
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='a_graph', component_property='figure')],
     [Input(component_id='select_something', component_property='value')]
)
def update_graph(option_selection):
    print(option_selection)
    print(type(option_selection))

    container = "The option chosen is: {}".format(option_selection)

    # update the data 
    dff = df.copy()
    print('copied')
    dff = dff[dff[' Hauptfach'] == option_selection]
    print('filtered', dff.shape)
    # create graph
    fig = px.scatter(
        data_frame = dff,
        x = ' Matrikel_nr',
        y = ' Fachsemester',
    )
    return container, fig



print("Ran through.")


if __name__ == '__main__':
   app.run_server(debug=True)