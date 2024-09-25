import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import  os

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']


patients=pd.read_csv('IndividualDetails.csv')
total=patients.shape[0]
active=patients[patients['current_status']=='Hospitalized'].shape[0]
Recovered=patients[patients['current_status']=='Recovered'].shape[0]
Deceased=patients[patients['current_status']=='Deceased'].shape[0]

options=[
    {'label':'All','value':'All'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deceased','value':'Deceased'}
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
    html.H1("Coronavirus Pandemic", style={'color': '#fff', 'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className='card-title'),
                    html.H4(total, className='card-text')
                ], className='card-body')
            ], className='card bg-danger text-white')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered", className='card-title'),
                    html.H4(Recovered, className='card-text')
                ], className='card-body')
            ], className='card bg-success text-white')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths", className='card-title'),
                    html.H4(Deceased, className='card-text')
                ], className='card-body')
            ], className='card bg-dark text-white')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", className='card-title'),
                    html.H4(active, className='card-text')
                ], className='card-body')
            ], className='card bg-warning text-white')
        ], className='col-md-3'),
    ], className='row'),
    html.Div([],className='row'),
    html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(id='picker',options=options, value='All'),
                        dcc.Graph(id='bar')
                    ],className='card-body')
                ],className='card')
            ],className='col-md-12')
    ],className='row')
], className='container')

@app.callback(
    Output('bar', 'figure'),
    [Input('picker', 'value')]
)
def update_graph(type):
    if type == 'All':
        pbar = patients['detected_state'].value_counts().reset_index()
        pbar.columns = ['detected_state', 'count']
        return {
            'data': [go.Bar(x=pbar['detected_state'], y=pbar['count'])],
            'layout': go.Layout(title='State Total Count')
        }
    else:
        npat = patients[patients['current_status'] == type]
        pbar = npat['detected_state'].value_counts().reset_index()  # Corrected here
        pbar.columns = ['detected_state', 'count']  # Ensure columns are correctly named
        return {
            'data': [go.Bar(x=pbar['detected_state'], y=pbar['count'])],
            'layout': go.Layout(title='State Total Count')
        }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))  # Default to port 8050 locally
    app.run_server(debug=True, host='0.0.0.0', port=port)
    app.run_server(debug=True)