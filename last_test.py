import pandas as pd
import sqlite3
import streamlit as st
from datetime import date
import numpy as np
import matplotlib.pyplot as plt

import os


def well_test():
    
    conn = sqlite3.connect('MyData.db')
    sql_query1 = '''  SELECT * FROM DPR

UNION ALL
SELECT 'Grand Total',  'Grand Total', SUM(NetOil),SUM(LastTest) ,SUM(DaysFromTest),NULL, NULL FROM DPR;
 '''
    sql_query2 = '''SELECT * FROM FPR

UNION ALL
SELECT 'Grand Total',  SUM(NetOil),SUM(LastTest),SUM(NetOilDiffer),SUM(DaysFromTest)  FROM FPR;
'''

    df_well = pd.read_sql_query(sql_query1,conn)
    df_field = pd.read_sql_query(sql_query2,conn)


    def sorted_bins(df):
         df = df[df['DaysFromTest'] > 29]
         df =df.sort_values(['NetOil'],ascending = False)
         return df


         
    def create_histogram(df, x):
        # Select the first column of the DataFrame
        df = df.iloc[:-1]
        df = df[df['DaysFromTest'] > 29]
        column = 'DaysFromTest'
        well_name_column = 'WellName'

        # Set the figure size
        plt.figure(figsize=(4, 2))  # Adjust the width and height according to your desired size

        # Create a histogram with specified number of bins
        n, bins, patches = plt.hist(df[column], bins=x, width=23)

        # Set labels and title for the histogram
        plt.xlabel(column, fontsize=6)  # Adjust the font size of the x-axis label
        plt.ylabel('Frequency', fontsize=6)  # Adjust the font size of the y-axis label
        plt.title(f'Histogram of {column}', fontsize=7)
        plt.locator_params(axis='x', nbins=23)
        plt.yticks(fontsize=3)
        plt.xticks(range(30, int(max(bins))+1, 10), fontsize=3)

        well_name_bins = []  # List to store filtered DataFrames for each bin

        # Filter the DataFrame and store filtered DataFrames for each bin
        for i in range(len(bins) - 1):
            filtered_df = df[df[column].between(bins[i], bins[i+1])]
            well_name_bins.append(filtered_df)

        # Display the y-values when hovering over the bins
        for i in range(len(patches)):
            plt.annotate(f'{int(n[i])}', xy=(bins[i], n[i]), xytext=(0, 5), textcoords='offset points',
                        ha='center', va='bottom', fontsize=6)

        # Display the histogram
        st.pyplot(plt)

        return well_name_bins

    tab1, tab2, tab3 = st.tabs(["DPR", "Test Statistics", "Pressure Statistics"])


    with tab1:
        col1,col2 = st.columns([1,1])
        with col1:
            y=df_well.iloc[-1]
            df_well = df_well.iloc[:-1].sort_values('DaysFromTest',ascending=False)
            df_well = df_well.append(y)
            today = df_well['Datee'][0]
            st.subheader(str(today))
            df_well=df_well.iloc[:,1:]
            df_well = df_well.reset_index(drop=True)
            st.markdown('<style>table.dataframe th, table.dataframe td {font-size: x-small;}</style>', unsafe_allow_html=True)
            st.dataframe(df_well)


        
        with col2:
            for i in range(2):
                st.write("")
            col3,col4 = st.columns([1,1])
            with col3:
                    but1= st.button('Export by wells')
                    st.dataframe(df_field)
            with col4:
                    but2 = st.button('Export by Field')  



    if but1:
        myfile = 'DPR.csv'
        df_well.to_csv(myfile)
        os.startfile(myfile)


    if but2:
        myfile2 = 'FPR.csv'
        df_field.to_csv(myfile2)
        os.startfile(myfile2)  




    with tab2:
         col12,col13 = st.columns([6,1])
         with col12:
              a=create_histogram(df_well, 9)
              col20,col21,col22,col23,col24,col25,col26,col27,col28 = st.columns([1,1,1,1,1,1,1,1,1])
              cols = [col20,col21,col22,col23,col24,col25,col26,col27,col28]
              for i ,col in enumerate(cols):
                   col.dataframe(a[i].reset_index(drop=True))

         with col13:
              df_sorted = sorted_bins(df_well)
              st.dataframe(df_sorted)          
              
             
                   
         
         
             

            
                           

                
                    
                
