# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 12:41:00 2023

@author: Tan7080
"""

import pandas as pd
import sqlite3
import numpy as np



conn = sqlite3.connect('MyData.db')

sql_query1 = '''SELECT 
    DailyProduction.Datee,
    DailyProduction.WellName,
    WellTest.GrossTest,
    WellTest.NetTest,
    WellTest.WcTest,
    DailyProduction.RunTime,
    Fields.Field
FROM 
    DailyProduction
LEFT JOIN Fields ON DailyProduction.WellName = Fields.WellName
LEFT JOIN WellTest ON DailyProduction.ID = WellTest.DailyProdID
WHERE Fields.Field NOT IN ('Ferdaus', 'Rawda','Rayan') 
ORDER BY DailyProduction.WellName, DailyProduction.Datee ;

    '''

sql_query2 = '''SELECT 
    DailyProduction.Datee,
    DailyProduction.WellName,
    CAST(DailyProduction.Gross AS INT) AS Gross,
    CAST(DailyProduction.NetOil AS INT) AS NetOil,

    CAST((DailyProduction.WaterProduced / CAST(DailyProduction.Gross AS REAL)) * 100 AS REAL) AS WC,
   
    DailyProduction.RunTime,
  
    Fields.Field
    
    FROM 
    DailyProduction
    
    
    LEFT JOIN Fields ON DailyProduction.WellName = Fields.WellName

    WHERE Fields.Field IN ('Ferdaus', 'Rawda','Rayan') 
     

     
'''

df1 = pd.read_sql_query(sql_query1, conn)

df2 = pd.read_sql_query(sql_query2, conn)
df2 = df2.rename(columns={'Gross': 'GrossTest', 'NetOil': 'NetTest', 'WC': 'WcTest'})
df = [df1,df2]
df=pd.concat(df)
#df['RunTime'] = pd.to_numeric(df['RunTime'], errors='coerce')
#df["RunTime"] = df["RunTime"].astype(float)
#df = df[df['RunTime']> 0]

fields_to_exclude = ['Ferdaus', 'Rayan', 'Rawda']
mask = ~df['Field'].isin(fields_to_exclude)


df.loc[mask, 'GrossTest'] = df.loc[mask, 'GrossTest'].fillna(method='ffill')
df.loc[mask, 'NetTest'] = df.loc[mask, 'NetTest'].fillna(method='ffill')
df.loc[mask, 'WcTest'] = df.loc[mask, 'WcTest'].fillna(method='ffill')

df = df.rename(columns={'GrossTest':'Gross',  'NetTest':'NetOil', 'WcTest':'WC' })
df = df.sort_values('Datee')
df.to_csv('TestDiffer.csv')
    