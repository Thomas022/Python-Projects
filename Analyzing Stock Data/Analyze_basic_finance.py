import codecademylib3_seaborn
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import pandas_datareader.wb as wb
import numpy as np

#using pandas to import csv
gold_prices = pd.read_csv('gold_prices.csv')
#print(gold_prices)

crude_oil_prices = pd.read_csv('crude_oil_prices.csv')
#print(crude_oil_prices)

#create two datetime variables
start = datetime(1999, 1, 1)
end = datetime(2019, 1, 1)

#Using FRED API to store Data
nasdaq_data = web.DataReader('NASDAQ100', 'fred', start, end)
#print(nasdaq_data)

sap_data = web.DataReader('SP500', 'fred', start, end)
#print(sap_data)

#Using wb.download function to get GDP data from the world BAnk API
gdp_data = wb.download(indicator='NY.GDP.MKTP.CD', country=['US'], start=start, end=end)

export_data = wb.download(indicator='NE.EXP.GNFS.CN', country=['US'], start=start, end=end)
#print(export_data)

#Creating a function to calculate Log Return
def log_return(prices):
  return np.log(prices / prices.shift(1))

gold_returns = log_return(gold_prices['Gold_Price'])

crudeoil_return = log_return(crude_oil_prices['Crude_Oil_Price'])

sap_return = log_return(sap_data['SP500'])

nasdaq_return = log_return(nasdaq_data['NASDAQ100'])

print('Gold', gold_returns.var())
print('crudeoil', crudeoil_return.var())
print('SAP', sap_return.var())
print('Nasdaq', nasdaq_return.var())
