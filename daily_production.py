# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 09:44:03 2023

@author: Tan7080
"""

import pandas as pd
import sqlite3
import streamlit as st
from bokeh.models import DatetimeTickFormatter, HoverTool,Title,LinearAxis, Range1d,NumeralTickFormatter
from bokeh.plotting import figure
import datetime
import math
import pandas as pd
from bokeh.palettes import Category10
import numpy as np

def daily_prod():
    
    col1, col2, col3, col4,col5 ,col6= st.columns([1, 1, 1, 1,0.5,0.5 ])
       
       
    df = pd.read_csv('daily.csv')
    df['NetOil'] = pd.to_numeric(df['NetOil'], errors='coerce')
    df['gross'] = pd.to_numeric(df['gross'], errors='coerce')
    df['wc'] = pd.to_numeric(df['wc'], errors='coerce')
   
    

    with col1:
        
        unique_fields = df['field'].unique().tolist()
        unique_fields.insert(0,'All feilds')
        selected_fields = st.multiselect("Select Field(s)", unique_fields)
           
      
        
    with col2:
        unique_WellName =df['well_name'].unique().tolist()
        unique_WellName.insert(0,'All wells')
        selected_well_names = st.multiselect("Select Well Name(s)", unique_WellName)
        
     
        
    with col3:
        unique_layers = df['layer'].unique().tolist()
        unique_layers.insert(0,'All layers')
        selected_layers = st.multiselect("Select Layer(s)", unique_layers)
       
    
  

    def create_plot(title_text, df, ymin=None, ymax=None):
        df = df.replace([np.inf, -np.inf], np.nan).dropna()
        
        title = Title(text=title_text, align="center", text_font_style="bold", text_font_size="18pt")
        p = figure(x_axis_label='Date', y_axis_label='Production', x_axis_type='datetime', width=800)
        p.background_fill_color = "lightblue"
        p.title = title
        p.border_fill_color = "lightblue"
        p.line(df['date'], df['NetOil'], color='green', legend_label='NetOil')
        p.line(df['date'], df['gross'], color='black', legend_label='Gross')
    
        # Add line for 'wc' column on secondary y-axis
        p.extra_y_ranges = {"wc_range": Range1d(start=0, end=df['wc'].max() * 1.1)}
        p.add_layout(LinearAxis(y_range_name="wc_range", axis_label='WC', axis_line_color='blue', axis_label_text_color='blue'), 'right')
        p.line(df['date'], df['wc'], color='blue', y_range_name="wc_range", legend_label='WC', line_dash='dashed')
    
        # Add line for 'cum_oil' column on third y-axis
        p.extra_y_ranges["cum_oil_range"] = Range1d(start=0, end=df['cum_oil'].max() * 1.1)
        p.add_layout(LinearAxis(y_range_name="cum_oil_range", axis_label='Cumulative Oil', axis_line_color='brown', axis_label_text_color='brown'), 'left')
        p.line(df['date'], df['cum_oil'], color='brown', y_range_name="cum_oil_range", legend_label='CumOil')
    
        p.xaxis.formatter = DatetimeTickFormatter(days='%Y-%m-%d', months='%Y-%m', years='%Y')
        p.xaxis.major_label_orientation = math.pi / 4  # Rotate x-axis labels for better readability
        num_intervals = 10
        interval_width = int(len(df) / num_intervals)
        p.xaxis.ticker.desired_num_ticks = num_intervals
        hover_tool = HoverTool(tooltips=[('x', '@x{%F}'), ('y', '@y')],
                               formatters={'@x': 'datetime'},
                               mode='vline')
        p.add_tools(hover_tool)
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"
        p.legend.label_text_color = 'rgb(0, 0, 0)'
        p.legend.label_text_font_size = '8pt'
        
        p.yaxis.formatter = NumeralTickFormatter(format='0,0')
    
        # Set the maximum value of the primary y-axis
        p.y_range.end = df['gross'].max() * 1.1
    
        # Set default values for ymin and ymax
        if ymin is not None:
            p.y_range.start = ymin
        if ymax is not None:
            p.y_range.end = ymax
      
  
        # Set y-axis formatter for normal numbers
        p.yaxis.formatter = NumeralTickFormatter(format='0,0')
    
        # Set the maximum value of the primary y-axis
        
    
        return p

    
    
    df_select = df[
    (
        (df['well_name'].isin(selected_well_names) if selected_well_names and 'All wells' not in selected_well_names else ~df.index.duplicated()) |
        ('All wells' in selected_well_names)
    ) &
    (
        (df['layer'].isin(selected_layers) if selected_layers and 'All layers' not in selected_layers else ~df.index.duplicated()) |
        ('All layers' in selected_layers)
    ) &
    (
        (df['field'].isin(selected_fields) if selected_fields and 'All fields' not in selected_fields else ~df.index.duplicated()) |
        ('All feilds' in selected_fields)
    )
]

    df1 = df_select.loc[:, 'layer'].to_frame()
    df1_unique = df1['layer'].drop_duplicates().to_frame()

     
    df_select = df_select.groupby('date').agg({'NetOil': 'sum', 'gross': 'sum', 'wc': 'sum'}).reset_index()      
    df_select['date'] = pd.to_datetime(df_select['date']).dt.date
    df_select = df_select.sort_values(['date'])
    df_select['cum_oil'] = df_select['NetOil'].cumsum()
    
    
    with col5:
      
        st.markdown("<h1 style='font-weight:bold; font-size:30px;'>#scale adjusting</h1>", unsafe_allow_html=True)
        y_min = st.number_input('Enter y_min:',0)
        for i in range(0,6):
            st.write(" ")
        min_date_input = st.text_input('Enter min date (yyyy-mm-dd):')
        st.dataframe(df1_unique)
       
    
        
    with col6:
       for i in range(1,8):
           st.write(" ")  
       y_max = st.number_input('Enter y_max:',0)
       for i in range(0,6):
           st.write(" ")
       max_date_input = st.text_input('Enter max date (yyyy-mm-dd)):')
       
       st.dataframe(df_select)
    
    
    
    
    if selected_well_names:
        my_title = selected_well_names[0] + "_" + selected_layers[0] if selected_layers else selected_well_names[0]
    
    else:
        my_title = 'All wells'

    
    
   
    if min_date_input and max_date_input:
        min_date_input = datetime.datetime.strptime(min_date_input, '%Y-%m-%d')
        max_date_input = datetime.datetime.strptime(max_date_input, '%Y-%m-%d')
        df_select['date'] = pd.to_datetime(df_select['date']).dt.date  # Convert to datetime.date
        df_select = df_select[(df_select['date'] >= min_date_input.date()) & (df_select['date'] <= max_date_input.date())]

        
       
       
    default_plot = create_plot(my_title, df_select)     
        
    if y_max :
        plot = create_plot(my_title, df_select, ymax=y_max)
    elif y_min:
        plot = create_plot(my_title, df_select, ymin=y_min)
    elif y_min and y_max:
        plot = create_plot(my_title, df_select, ymin=y_min,ymax=y_max)
    else:
        plot = default_plot      
        
    
    
    with col1:
        if df_select.empty:
            st.write("No data available for the selected well name and layer combination.")
        else:
            st.bokeh_chart(plot)
            
            
   
        
        
       
 
    
        
    