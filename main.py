import pandas as pd
import numpy as np
import matplotlib.pyplot as plot

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

fig, ax = plot.subplots()
ax.plot(dfComebacksByYear['Year'],dfComebacksByYear['# Comebacks'], linewidth= 2.0)
plot.show()
print(dfComebacksByTeam)
dfComebacksByTeam.to_csv('ByTeam.csv')
