import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from data_prepare import coin_set, df_coin


app = dash.Dash()
server = app.server

app.layout = html.Div([
   
    html.H1("Coin Price Analysis Dashboard", style={"textAlign": "center"}),
   
    dcc.Tabs(id="tabs", children=[
       
        dcc.Tab(label='Predict Coin Price',children=[

			html.Div([
                html.H1("Choose coin", 
                        style={'textAlign': 'center'}),
              
                dcc.Dropdown(id='my-coin-dropdown',
                             options=[{'label': 'BTC-USD', 'value': 'BTC'},
                                      {'label': 'ETH-USD','value': 'ETH'}, 
                                      {'label': 'ADA-USD', 'value': 'ADA'}], 
                             multi=False,
                             value='BTC',
                             style={"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),

				html.H2("Actual closing price",style={"textAlign": "center"}),
				dcc.Graph(id="Actual Data"),
				
                html.H2("LSTM Predicted closing price",style={"textAlign": "center"}),
				dcc.Graph(id="Predicted Data")				
			])        		


        ]),
        dcc.Tab(label='Coin Price Data', children=[
            html.Div([
                html.H1("Stocks High vs Lows", 
                        style={'textAlign': 'center'}),
              
                dcc.Dropdown(id='my-dropdown',
                             options=[{'label': 'Bitcoin - USD', 'value': 'BTC'},
                                      {'label': 'Ethereum - USD','value': 'ETH'}, 
                                      {'label': 'Cardano - USD', 'value': 'ADA'}], 
                             multi=True,value=['BTC'],
                             style={"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),
                dcc.Graph(id='highlow'),
                html.H1("Stocks Market Volume", style={'textAlign': 'center'}),
         
                dcc.Dropdown(id='my-dropdown2',
                             options=[{'label': 'Bitcoin', 'value': 'BTC'},
                                      {'label': 'Ethereum','value': 'ETH'}, 
                                      {'label': 'Cardano', 'value': 'ADA'}], 
                             multi=True,value=['BTC'],
                             style={"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),
                dcc.Graph(id='volume')
            ], className="container"),
        ])
    ])
])


@app.callback([Output('Actual Data', 'figure'), Output('Predicted Data', 'figure')],
              Input('my-coin-dropdown', 'value'))
def update_graph(selected_dropdown):
    trace1 = []
    trace2 = []
    figure1={
        "data":[
            go.Scatter(
                x=coin_set[selected_dropdown][0].index,
                y=coin_set[selected_dropdown][1]["Close"],
                mode='markers'
            )
        ],
        "layout":go.Layout(
            title='scatter plot',
            xaxis={'title':'Date'},
            yaxis={'title':'Closing Rate'}
        )
    }

    figure2={
        "data":[
            go.Scatter(
                x=coin_set[selected_dropdown][1].index,
                y=coin_set[selected_dropdown][1]["Predictions"],
                mode='markers'
            )
        ],
        "layout":go.Layout(
            title='scatter plot',
            xaxis={'title':'Date'},
            yaxis={'title':'Closing Rate'}
        )
    }
    return [figure1, figure2]




@app.callback(Output('highlow', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown):
    dropdown = {"BTC": "Bitcoin","ETH": "Ethereum","ADA": "Cardano",}
    trace1 = []
    trace2 = []
    for stock in selected_dropdown:
        trace1.append(
          go.Scatter(x=df_coin[stock]["Date"],
                     y=df_coin[stock]["High"],
                     mode='lines', opacity=0.7, 
                     name=f'High {dropdown[stock]}',textposition='bottom center'))
        trace2.append(
          go.Scatter(x=df_coin[stock]["Date"],
                     y=df_coin[stock]["Low"],
                     mode='lines', opacity=0.6,
                     name=f'Low {dropdown[stock]}',textposition='bottom center'))
    traces = [trace1, trace2]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                            '#FF7400', '#FFF400', '#FF0056'],
            height=600,
            title=f"High and Low Prices for {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': True}, 'type': 'date'},
             yaxis={"title":"Price (USD)"})}
    return figure


@app.callback(Output('volume', 'figure'),
              [Input('my-dropdown2', 'value')])
def update_graph(selected_dropdown_value):
    dropdown = {"BTC": "Bitcoin","ETH": "Ethereum","ADA": "Cardano",}
    trace1 = []
    for stock in selected_dropdown_value:
        trace1.append(
          go.Scatter(x=df_coin[stock]["Date"],
                     y=df_coin[stock]["Volume"],
                     mode='lines', opacity=0.7,
                     name=f'Volume {dropdown[stock]}', textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data, 
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                            '#FF7400', '#FFF400', '#FF0056'],
            height=600,
            title=f"Market Volume for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M',
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': True}, 'type': 'date'},
             yaxis={"title":"Transactions Volume"})}
    return figure



if __name__=='__main__':
	app.run_server(debug=True)