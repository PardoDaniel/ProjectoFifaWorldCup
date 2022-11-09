# -----------------------------------------------Importacion de las librerias requeridas------------------------------------------------------------------------#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from turtle import width
import dash
from dash import dcc, dash_table
from dash import html
from dash.dependencies import Input, Output
from datetime import date

# -------------------------------------------------------------------------------------------------------------------------------------------------------------#
# --------------------------------------------------------Perparacion de los datos ----------------------------------------------------------------------------#
df = pd.read_csv('WorldCupMatches.csv')

df = df[['Year','Stadium', 'City','Home Team Name','Home Team Goals','Away Team Goals','Away Team Name','Half-time Home Goals','Half-time Away Goals']]
conditionsWin = [(df['Home Team Goals']>df['Away Team Goals']),
                (df['Away Team Goals' ]> df['Home Team Goals']),
                (df['Home Team Goals'] == df['Away Team Goals'])
              ]
valuesWin= [df['Home Team Name'],df['Away Team Name'],'Tie']
df['Winner'] = np.select(conditionsWin, valuesWin)

conditionsLeading = [(df['Half-time Home Goals']>df['Half-time Away Goals']),
                (df['Half-time Away Goals' ]> df['Half-time Home Goals']),
                (df['Half-time Home Goals'] == df['Half-time Away Goals'])
              ]

valuesLeading =[df['Home Team Name'],df['Away Team Name'],'Tie']

df['Leading at Half-time'] = np.select(conditionsLeading,valuesLeading)

conditionsComeback = [(df['Winner'] == df['Leading at Half-time']),
                (df['Leading at Half-time' ] == 'Tie'),
                (df['Winner'] != df['Leading at Half-time'])
              ]
valuesComeback = ['False','False','True']

df['Comeback after Half-time'] = np.select(conditionsComeback,valuesComeback)

dfComebacksByYear = df.groupby('Year')['Comeback after Half-time'].apply(lambda x: (x=='True').sum()).reset_index(name='# Comebacks')
dfComebacksByTeam = df.groupby('Winner')['Comeback after Half-time'].apply(lambda x: (x=='True').sum()).reset_index(name='# Comebacks')



# -------------------------------------------------------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------------App creation-------------------------------------------------------------------------------------------#
app = dash.Dash(__name__)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------------App Layout---------------------------------------------------------------------------------------------#
app.layout = html.Div([
    html.H1("World Cup Archive", style={'text-align': 'center','font-family': ''''Oswald', Helvetica, sans-serif''','font-size': '100px','transform': 'skewY(0deg)',
                                        'letter-spacing': '4px',
                                          'word-spacing': '-8px',
                                          'color': '''#C00000''',
                                          'text-shadow':''' 
                                          -1px -1px 0 #C00000,
                                          -2px -2px 0 #F7B32D,
                                          -3px -3px 0 #F7B32D,
                                          -4px -4px 0 #F7B32D,
                                          -5px -5px 0 #F7B32D,
                                          -6px -6px 0 #F7B32D,
                                          -7px -7px 0 #F7B32D,
                                          -8px -8px 0 #F7B32D,
                                          -30px 20px 30px #afafaf'''
                                        }),
    dcc.DatePickerRange(id='date-picker-range',
        start_date=date(1930, 1, 1),
        end_date_placeholder_text='Select a date!'),   
    html.Div(id='output_container', children=[]),
    html.Br(),
    dash_table.DataTable(
    data=dfComebacksByTeam.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in dfComebacksByTeam.columns],
    )
])

# TODO------------------------------------ MAIN AND RUNNING OF APP----------------------------------------------------------------------------------------------# 
if __name__ == '__main__':
    app.run_server(debug= True)
# TODO------------------------------------ MAIN AND RUNNING OF APP----------------------------------------------------------------------------------------------# 