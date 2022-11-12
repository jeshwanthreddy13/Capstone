import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import datetime
import pandas as pd
import numpy as np
ticker_name = "SPY"
stocks = [ticker_name]
start = datetime.datetime(2022,1,9)
end = datetime.datetime(2022,10,9)
df = yf.download(stocks, start=start, end=end)
print(df.shape[0])
#print(df.head())
df=df[df['Volume']!=0]#Remove all rows whose volume is equal to zero
df.reset_index(drop=True, inplace=True)#Reset the Index
df.isna().sum()

#Support and Resistance Functions

def is_support(dataFrame, row, param_1, param_2):
    for i in range(row-param_1+1, row+1):
        if(dataFrame.Low[i]>dataFrame.Low[i-1]):
            return False
    for i in range(row+1,row+param_2+1):
        if(dataFrame.Low[i]<dataFrame.Low[i-1]):
            return False
    return True


def is_resistance(dataFrame, row, param_1, param_2):
    for i in range(row-param_1+1, row+1):
        if(dataFrame.High[i]<dataFrame.High[i-1]):
            return False
    for i in range(row+1,row+param_2+1):
        if(dataFrame.High[i]>dataFrame.High[i-1]):
            return False
    return True

Support_Ressistance_Values = list();
param_1=2;
param_2=3;
for row in range(3, df.shape[0]- param_2):
    if is_support(df, row, param_1, param_2):
        Support_Ressistance_Values.append((row,df.Low[row],1))
    if is_resistance(df, row, param_1, param_2):
        Support_Ressistance_Values.append((row,df.High[row],2))
        
#print(Support_Ressistance_Values)

#**********   PRINT THE LINES ON THE GRAPH *******#

'''

xaxis_Start = 0
xaxis_End = df.shape[0] + 3
count=0
df_partial = df[xaxis_Start:xaxis_End]
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt

fig = go.Figure(data=[go.Candlestick(x=df_partial.index,
                open=df_partial['Open'],
                high=df_partial['High'],
                low=df_partial['Low'],
                close=df_partial['Close'])])

while (True):
    if(count>len(Support_Ressistance_Values)-1 ):
        break
    fig.add_shape(type='line', x0=xaxis_Start, y0=Support_Ressistance_Values[count][1],
                  x1=xaxis_End,
                  y1=Support_Ressistance_Values[count][1],line=dict(color="RoyalBlue",width=1)
                  )
    count+=1
fig.show()


'''


#********  USED TO INCREASE SENSITIVITY ******#
sensitivity = 0.1



Final_Supports = [val[1] for val in Support_Ressistance_Values if val[2]==1]
Final_Ressistances = [val[1] for val in Support_Ressistance_Values if val[2]==2]
Final_Supports.sort()
Final_Ressistances.sort()

for i in range(1,len(Final_Supports)):
    if(i>=len(Final_Supports)):
        break
    if abs(Final_Supports[i]-Final_Supports[i-1])<=(df['High'].mean())*sensitivity:Final_Supports.pop(i)

for i in range(1,len(Final_Ressistances)):
    if(i>=len(Final_Ressistances)):
        break
    if abs(Final_Ressistances[i]-Final_Ressistances[i-1])<=(df['High'].mean())*sensitivity:Final_Ressistances.pop(i)
#print(Final_Ressistances)
#print(Final_Supports)



#**********   PRINT THE NEW LINES(MORE SENSITIVE LINES) *******#



Xaxis_Start = 0
Xaxis_End = 200
count=0
df_partial = df[Xaxis_Start:Xaxis_End]


fig = go.Figure(data=[go.Candlestick(x=df_partial.index,
                open=df_partial['Open'],
                high=df_partial['High'],
                low=df_partial['Low'],
                close=df_partial['Close'])])




while (True):
    if(count>len(Final_Supports)-1 ):
        break
    fig.add_shape(type='line', x0=Xaxis_Start, y0=Final_Supports[count],
                  x1=Xaxis_End,
                  y1=Final_Supports[count],
                  line=dict(color="RoyalBlue",width=2)
                  )
    count+=1

count=0
while (True):
    if(count>len(Final_Ressistances)-1 ):
        break
    fig.add_shape(type='line', x0=Xaxis_Start, y0=Final_Ressistances[count],
                  x1=Xaxis_End,
                  y1=Final_Ressistances[count],
                  line=dict(color="RoyalBlue",width=2)
                  )
    count+=1

fig.show()

Sensitive_values = []

Sensitive_values.extend(Final_Ressistances)
Sensitive_values.extend(Final_Supports);

Final_df = pd.DataFrame(Sensitive_values,columns =['Values']);
#Final_df.head()
