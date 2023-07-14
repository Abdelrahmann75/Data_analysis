# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:23:15 2023

@author: Tan7080
"""

import pandas as pd
import sqlite3

conn = sqlite3.connect("MyData.db")

sql_query1 = '''SELECT 
    DailyProduction.Datee,
    DailyProduction.WellName,
    CAST(DailyProduction.Gross AS INT) AS Gross,
    CAST(DailyProduction.NetOil AS INT) AS NetOil,

    CAST((DailyProduction.WaterProduced / CAST(DailyProduction.Gross AS REAL)) * 100 AS REAL) AS WC,
    DailyProduction.RunTime,
    WellTest.GrossTest,
    Fields.Field
FROM 
    DailyProduction
         
       
     LEFT JOIN Fields ON DailyProduction.WellName = Fields.WellName
     LEFT JOIN WellTest ON DailyProduction.ID = WellTest.DailyProdID

     
     
        '''
    
df1 = pd.read_sql_query(sql_query1, conn)



df1['datee&well1'] = df1['Datee'] + df1['WellName']

sql_query2 = "SELECt * FROM Layers"
df2 = pd.read_sql_query(sql_query2, conn)

df2['date&well2'] = df2['Date']+df2['WellName']

merged_df = pd.merge(df1, df2, left_on='datee&well1', right_on='date&well2',how = 'left')

df = merged_df.iloc[:,[0,1,2,3,4,5,6,7,11]]
df = df.rename(columns={"WellName_x":"well_name","Gross":"gross","GrossTest":"gross_test","WC":"wc","Field":"field","Layer":"layer","RunTime":"run_time","Datee":"date"})
df['gross_test'].fillna('', inplace=True)
df['wc'].fillna('', inplace=True)
df = df.sort_values(['well_name', 'date'])
df['layer'] = df['layer'].fillna(method='ffill')
df['date'] = pd.to_datetime(df['date'])

df.to_csv('daily.csv')