# -*- coding: utf-8 -*-
"""
Created on Mon May 29 12:59:38 2023

@author: Tan7080
"""

import pandas as pd
import numpy as np
import sqlite3

#connecting to sql and geting the max ID to update after
conn = sqlite3.connect('MyData.db')
print('connectino is ready')


sql_query = 'SELECT MAX(ID) FROM DailyProduction'

df_max = pd.read_sql_query(sql_query,conn)




x = df_max['MAX(ID)'][0]





#adding columns to data frame , to match the sql tables
df = pd.read_csv('C:/Users/tan7080/Desktop/production reports/my_update\mydata.csv')

df['WaterProduced'] =df['gross'] - df['net_oil']
df['ID'] = range(x + 1,(x +1)+len(df))
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')



#creating prod table
daily_prod = df.loc[:,['ID','date','well_name3','gross','net_oil','WaterProduced','gas','run_time']]

my_list = ['ID','Datee','WellName','Gross','NetOil','WaterProduced','Gas','RunTime']

for i,cell in enumerate(my_list):
    
    daily_prod.rename(columns={daily_prod.columns[i]:cell},inplace = True)
    



#creating well test table
well_test = df.loc[:,['ID','gross_test','net_oil_test','wc-Test']]

well_test.dropna(subset=['gross_test'], inplace=True)

my_list = ['DailyProdID','GrossTest','NetTest','WcTest']

for i,cell in enumerate(my_list):
    
    well_test.rename(columns={well_test.columns[i]:cell},inplace = True)
    



#creating Pip table table
pip_data = df.loc[:,['ID','pump_intake']]

pip_data.dropna(subset=['pump_intake'], inplace=True)

pip_data.rename(columns={'ID': 'DailyProdID'}, inplace=True)

pip_data.rename(columns={'pump_intake': 'PiP'}, inplace=True)

#updating sql tables form those data frames
print('starting data migration')

conn = sqlite3.connect('MyData.db')

daily_prod.to_sql('DailyProduction',conn,if_exists='append',index = False)
print('production done')

well_test.to_sql('WellTest',conn,if_exists='append',index = False)
print('wellTest done')

pip_data.to_sql('PiPData',conn,if_exists='append',index = False)
print('pressure done')




conn.commit()
conn.close()

