# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 15:02:01 2023

@author: Tan7080
"""

import streamlit as st


from daily_production import daily_prod
from prod_differ import differ
from filedoc import filing
from last_test import well_test






def main():
 
    st.set_page_config(layout="wide")
    menu = ["Daily Production","production differ","Well Test","Daily filing"]

# Iterate over the menu items and display them with spacing

    choice = st.sidebar.radio("Menu", menu)

    
    if choice == "Daily Production":
       	daily_prod()

    elif choice == "production differ":
         differ()

    elif choice == "Well Test":
         well_test()     
         
    elif choice == "Daily filing":
         filing()   
    
       
        
        
if __name__ == "__main__":
   main()
