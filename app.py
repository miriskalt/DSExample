'''
Sample Dash Dashboard for DS Project
'''
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px



app = dash.Dash(__name__)
server = app.server

### Import data

df = pd.read_csv('./data/sleep_stree_readiness.csv')


### App layout

app.layout = html.Div([
    html.H1("This is a sample project using human data", style={'text-align': 'center'}),
    html.H3("Linegraph of single feature over entire timespan", style={'text-align': 'center'}),

    html.P('The following interactive linegraph visualizes the selected features over the entire timespan of the dataset'),


    dcc.Dropdown(id="feature_selection",
                 options=[
                     {'label': "Deep Sleep in Minutes", 'value': 'deep_sleep_in_minutes'},
                     {'label': "Overall Score", 'value': 'overall_score'},
                     {'label': "Readiness Score", 'value': 'readiness_score_value'}],
                 multi=False,
                 value='overall_score', # init value
                 style={'width': '40%'}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(), # whitespace

    dcc.Graph(id='full_line_single_graph', figure={}),

    html.H3("Linegraph of all features over entire timespan", style={'text-align': 'center'}),

    dcc.Graph(id='full_line_all_graph', figure={}),


    html.H3("Research Question 1: What is the avg Readiness Score per Weekday?",
             style={'text-align': 'center'}),
    dcc.Graph(id='avg_readiness_day', figure={}),

    ])

### Callbacks
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='full_line_single_graph', component_property='figure')],
     [Input(component_id='feature_selection', component_property='value')]
)
def update_graph(option_selection):
    '''Update the overall linegraph'''
    container = f"The plot shows: {option_selection}"
    # create graph
    fig = px.line(
        data_frame = df,
        x = 'timeCode_x',
        y = option_selection,
        range_y=[0,100]
    )
    return container, fig






@app.callback(
     Output(component_id='full_line_all_graph', component_property='figure'),
     [Input(component_id='feature_selection', component_property='value')])
def update_all_graph(toggled):
    '''update the graph containing all features'''
    print('graph triggered')

    # create graph
    fig = px.line(
        data_frame = df,
        x = 'timeCode_x',
        y = ['STRESS_SCORE', 'overall_score', 'readiness_score_value'],
        labels=['stress', 'sleep', 'readiness'],
        range_y=[0,150]
    )
    print('graph created')
    return fig



@app.callback(
     Output(component_id='avg_readiness_day', component_property='figure'),
     [Input(component_id='feature_selection', component_property='value')])
def update_weekday_readiness_graph(toggled):
    '''mid-interactive bar plot of weekday readiness'''

    fig = px.histogram(df,
                       x="weekday",
                       y="readiness_score_value",
                       histfunc='avg',
                       range_y=[0,100],
                       category_orders={"weekday":["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}

                       )
    print('graph created')
    return fig







if __name__ == '__main__':
   app.run_server(debug=True)