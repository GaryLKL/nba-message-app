import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go
import matplotlib
import pandas as pd, numpy as np

df = pd.read_csv('finalGameBoxScore.csv')

df1 = df.query("GameIndex == 1 and HomeAway == 'Home'").drop("GameIndex", axis = 1).reset_index(drop=True)
df2 = df.query("GameIndex == 1 and HomeAway == 'Away'").drop("GameIndex", axis = 1).reset_index(drop=True)

df1_short = df1.drop(["Date", "Team", "HomeAway"], axis = 1).reset_index(drop = True)
df2_short = df2.drop(["Date", "Team", "HomeAway"], axis = 1).reset_index(drop = True)



def getSecond(timeString):
    MinSecond = [60, 1]
    sec = sum([m * s for m, s in zip(MinSecond,
                         map(int, timeString.split(":")))])
    return sec

colors = {
    'text': '#000000',
    'colorbar':list(matplotlib.colors.cnames.keys())
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children = df1["Date"][0],
        style={
            'textAlign': 'left',
            'color': colors['text'],
            'fontSize': 40
        }),
    html.H2(children = df1["Team"][0] + '  ( '+ str(sum(df1['PTS'])) + ' ) ',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'fontSize': 20
        }),
    html.Div([
        dash_table.DataTable(
        id = "table",
        data = df1_short.to_dict("records"),
        columns = [{"name": i, "id": i} for i in df1_short.columns],
        style_data_conditional=[

            {
                'if': {
                    'column_id': 'PTS',
                    'filter_query': '{PTS} >= 20'
            },
                'backgroundColor': 'yellow',
                'color': 'black'
            },
            {
                'if': {
                    'column_id': 'TRB',
                    'filter_query': '{TRB} >= 10'
            },
                'backgroundColor': 'yellow',
                'color': 'black'
            },
                     {
                'if': {
                    'column_id': 'AST',
                    'filter_query': '{AST} >= 10'
            },
                'backgroundColor': 'yellow',
                'color': 'black'
            },
            {
                'if': {
                    'filter_query': '{PTS} >= 10 && {AST} >= 10 && {TRB} >= 10'
            },
                'color': 'red'
            }  
        ],
        style_as_list_view = True, 
        style_table={'overflowX': 'scroll'},
        style_cell={
        'minWidth': '50px', 'maxWidth': '200px',
        'whiteSpace': 'no-wrap',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        },
        style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
        },
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        #fixed_columns={'headers': True, 'data': 3},
        ),
        html.Br(),
        html.H2(children = df2["Team"][0] + '  ( '+ str(sum(df2['PTS'])) + ' ) ',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'fontSize': 20
        }),
        dash_table.DataTable(
        id = "table2",
        data = df2_short.to_dict("records"),
        columns = [{"name": i, "id": i} for i in df2_short.columns],
        style_data_conditional=[

            {
                'if': {
                    'column_id': 'PTS',
                    'filter_query': '{PTS} >= 20'
            },
                'backgroundColor': 'orange',
                'color': 'black'
            },
            {
                'if': {
                    'column_id': 'TRB',
                    'filter_query': '{TRB} >= 10'
            },
                'backgroundColor': 'orange',
                'color': 'black'
            },
                     {
                'if': {
                    'column_id': 'AST',
                    'filter_query': '{AST} >= 10'
            },
                'backgroundColor': 'orange',
                'color': 'black'
            },
            {
                'if': {
                    'filter_query': '{PTS} >= 10 && {AST} >= 10 && {TRB} >= 10'
            },
                'color': 'red'
            }  
        ],
        style_as_list_view = True, 
        style_table={'overflowX': 'scroll'},
        style_cell={
        'minWidth': '50px', 'maxWidth': '200px',
        'whiteSpace': 'no-wrap',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        },
        style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
        },
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        #fixed_columns={'headers': True, 'data': 3},
        )]

    ),

    html.Div(
    className = 'row',
    children = [
        dcc.Graph(
            id='Graph1',
            figure={
                'data': [
                    {'x': df1["Players"], 'y': df1["PTS"], 'type': 'bar', 'name': 'PTS'},
                    {'x': df1["Players"], 'y': df1["AST"], 'type': 'bar', 'name': 'AST'},
                    {'x': df1["Players"], 'y': df1["TRB"], 'type': 'bar', 'name': 'TRB'}
                ],
                'layout': {
                    'title': 'Points, Assists, and Rebounds ( ' + df1["Team"][0] + ' )',
                    'fontSize': 30,
                    'font': {
                        'color': colors['text']
                    },
                    'xaxis': {
                        'title': 'Players'
                    },
                    'yaxis': {
                        'title': 'Counts'
                    }
                }
            }
        ),
        dcc.Graph(
            id='Graph3',
            figure={
                'data': [
                    go.Scatter(
                        x=df1["MP"].apply(getSecond),
                        y=df1["+/-"],
                        text = df1["Players"],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 20,
                            'line': {'width': 0.5, 'color': 'white'},
                            'color': colors["colorbar"][12:200:11][0:df1.index.__len__()]
                        },
                        
                    ) 
                ],
                'layout': go.Layout(
                    xaxis={'type': 'log', 'title': 'Time (Seconds Played)'},
                    yaxis={'title': '+ / -'},
                    title={'text': 'Plus / Minus ( ' + df1['Team'][0] + ' )'}

                ),

            }
        )
    ],
    style = {'width': '49%', 'display': 'inline-block'},
    ),
    html.Div(
    className = 'row',
    children = [
        dcc.Graph(
            id='Graph2',
            figure={
                'data': [
                    {'x': df2["Players"], 'y': df2["PTS"], 'type': 'bar', 'name': 'PTS'},
                    {'x': df2["Players"], 'y': df2["AST"], 'type': 'bar', 'name': 'AST'},
                    {'x': df2["Players"], 'y': df2["TRB"], 'type': 'bar', 'name': 'TRB'}
                ],
                'layout': {
                    'title': 'Points, Assists, and Rebounds ( ' + df2["Team"][0] + ' )',
                    'fontSize': 30,
                    'font': {
                        'color': colors['text']
                    },
                    'xaxis': {
                        'title': 'Players'
                    },
                    'yaxis': {
                        'title': 'Counts'
                    }
                }
            }
        ),
        dcc.Graph(
            id='Graph4',
            figure={
                'data': [
                    go.Scatter(
                        x=df2["MP"].apply(getSecond),
                        y=df2["+/-"],
                        text = df2["Players"],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 20,
                            'line': {'width': 0.5, 'color': 'white'},
                            'color': colors["colorbar"][12:200:11][0:df2.index.__len__()]
                        },
                        
                    ) 
                ],
                'layout': go.Layout(
                    xaxis={'type': 'log', 'title': 'Time (Seconds Played)'},
                    yaxis={'title': '+ / -'},
                    title={'text': 'Plus / Minus ( ' + df2['Team'][0] + ' )'}

                ),

            }
        )],
    style= {'width': '49%', 'display': 'inline-block'},
    ),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': df1['Team'][0], 'value': 'NYC'},
            {'label': df2['Team'][0], 'value': 'MTL'}
        ],
        value='NYC'
    )]
)



if __name__ == '__main__':
    app.run_server(debug=True)

