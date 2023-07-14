

import pandas as pd
import numpy as np
import dateutil.parser as dparser
import glob


dh = []

for infile in glob.glob("*.xlsm"):
    
            df = pd.read_excel(infile,sheet_name = 'Remarks')
                               
                              
            '''creating the Esp sensor data frame'''                 
        
            def contains_ESP(cell):
                    if isinstance(cell, str) and 'ESP sensor data :' in cell:
                            return True
                    else:
                            return False
                    
                    # Use applymap() to check all cells in the DataFrame for the word 'ESP sensor data :'
            mask = df.applymap(contains_ESP)
                    
                    # Find the indices of all rows and columns that contain the word 'ESP sensor data :'
            rows, cols = np.where(mask)
                    
            row= rows[0]
            col = cols[0]
                
                            
            df1=df.iloc[row + 3:,col:col+7]
            
            MyList = ['well_name1','fq','current','pi','pd','ti','tm']
                       
            for i,cell in enumerate(MyList):
                df1 = df1.rename(columns={df1.columns[i]: cell})
                
                
            df1.iloc[:, 1:] = df1.iloc[:, 1:].apply(pd.to_numeric, errors='coerce') 
            
           
            d = {"(?i)Fer?daus":"FER",
                "(?i)Rawda":"RAWDA",
                "(?i)central":"CENTRAL",
                "(?i)Ganna":"GAN",
                "(?i)GAN West":"GAN-West",
                "(?i)Abrar":"ABRAR",
                "(?i) SoutH":"- S",
                "(?i) East": "-E",
                "(?i)AS":"ABRAR- S",
                "(?i)Rayan":"RAYAN",
                 "(?i)SIDRA":"Sidra",
                 "(?i)^S-" : "Sidra-",
                 "(?i)^A-" : "ARBAR-",
                 "(?i)^r-": "RAWDA-",
                 "(?i)^g-": "GAN-",
               
                 
                 
                #remove brackets with numbers inside
                "\([^)]+\)":""}
            
            for key,value in d.items():
                df1["well_name1"].replace(key,value,regex=True,inplace=True)
            
            #remove leading and preceding whitespaces
            df1["well_name1"]=df1["well_name1"].str.strip()
            
            df1.dropna(subset=['well_name1'], inplace=True)
            
           
            
            
            '''creating the fluid_level data frame'''
            
            
            df2=pd.read_excel(infile,sheet_name = 'Fluid shots',skiprows=1)
            
            df2=df2.iloc[:,[1,2,4]]
            
            MyList = ['well_name2','fluid_level','pi']
                       
            for i,cell in enumerate(MyList):
                df2 = df2.rename(columns={df2.columns[i]: cell})
                
              
            d = {"(?i)Fer?daus":"FER",
                "(?i)Rawda":"RAWDA",
                "(?i)central":"CENTRAL",
                "(?i)Ganna":"GAN",
                "(?i)GAN West":"GAN-West",
                "(?i)Abrar":"ABRAR",
                "(?i) SoutH":"- S",
                "(?i) East": "-E",
                "(?i)AS":"ABRAR- S",
                "(?i)Rayan":"RAYAN",
                 "(?i)SIDRA":"Sidra",
                 "(?i)^S-" : "Sidra-",
                 "(?i)^A-" : "ARBAR-",
                 "(?i)^r-": "RAWDA-",
                 "(?i)^g-": "GAN-",
                 "(?i)ABRAR S-": "ABRAR- S-",
                 
                 
                 
                #remove brackets with numbers or letters inside
                "\([^)]+\)":""}
            
            for key,value in d.items():
                df2["well_name2"].replace(key,value,regex=True,inplace=True)
            
            #remove leading and preceding whitespaces
            df2["well_name2"]=df2["well_name2"].str.strip()
            
            
            df2.dropna(subset=['well_name2'], inplace=True)
            
            df2 = df2.drop_duplicates(subset=['well_name2'], keep='first')
           
            
           
        
            
            '''creating the production data frame'''      
            
            df3= pd.read_excel(infile,sheet_name='Report',skiprows = 7)
            
                    
            df3 = df3.rename(columns={df3.columns[0]: 'Fields'})
            
            Total_row = df3[df3['Fields'].str.contains('TOTAL', case=True, na=False)].index[0]
            
            Last_row = Total_row - 1
            
            df3 = df3.iloc[:Last_row]
            
            df3 =df3.iloc[:,[1,3,4,6,8,9,11,12]]
            
            MyList = ['well_name3','pump_type','gross','net_oil','run_time','w.c','gas','gor']
                    
            for i,cell in enumerate(MyList):
                df3 = df3.rename(columns={df3.columns[i]: cell})
            
            pd.set_option('display.max_rows', None)
            
            
            d = {"(?i)Fer?daus":"FER",
                "(?i)Rawda":"RAWDA",
                "(?i)central":"CENTRAL",
                "(?i)Ganna":"GAN",
                "(?i)GAN West":"GAN-West",
                "(?i)Abrar":"ABRAR",
                "(?i) SoutH":"- S",
                "(?i) East": "-E",
                "(?i)AS":"ABRAR- S",
                "(?i)Rayan":"RAYAN",
                 "(?i)SIDRA":"Sidra",
                 "(?i)^S-" : "Sidra-",
                 "(?i)^A-" : "ARBAR-",
                 "(?i)^r-": "RAWDA-",
                 "(?i)^g-": "GAN-",
                 "(?i)Abrar -":"ABRAR-",
                 "(?i)RAWDA-E-1":"RAWDA-E",
                 
                
                
                
                 
                 
                #remove brackets with numbers inside
             "\([^)]+\)":""}
            
            for key,value in d.items():
                df3["well_name3"].replace(key,value,regex=True,inplace=True)
            
            #remove leading and preceding whitespaces
            df3["well_name3"]=df3["well_name3"].str.strip()
            
            df3
            
            
            
            
            '''creating the well test data frame'''  
            
            df4= pd.read_excel(infile,sheet_name='Test data',skiprows = 2)
            
            df4 =df4.iloc[:,[1,4,5,6,7,8]]
            
            
            MyList = ['well_name4','gross_test','wc-Test','net_oil_test','gas_test','test_time']
                    
            for i,cell in enumerate(MyList):
                df4 = df4.rename(columns={df4.columns[i]: cell}) 
            
            df4 = df4.dropna(subset=['well_name4'])
            
            
            
            
            
            '''creating the events data frame'''  
            
            df5= pd.read_excel(infile,sheet_name='Remarks')
            
            df5=df5.iloc[:,1:3]
            
            df5 = df5.rename(columns={df5.columns[0]: 'well_name5',df5.columns[1]:'events'})
            
            df5 = df5.dropna(subset=['well_name5'])
            
            df5 = df5.drop_duplicates(subset=['well_name5'], keep='first')
            
            d = {"(?i)Fer?daus":"FER",
                "(?i)Rawda":"RAWDA",
                "(?i)central":"CENTRAL",
                "(?i)Ganna":"GAN",
                "(?i)GAN West":"GAN-West",
                "(?i)Abrar":"ABRAR",
                "(?i) SoutH":"- S",
                "(?i) East": "-E",
                "(?i)AS":"ABRAR- S",
                "(?i)Rayan":"RAYAN",
                 "(?i)SIDRA":"Sidra",
                 "(?i)^S-" : "Sidra-",
                 "(?i)^A-" : "ARBAR-",
                 "(?i)^r-": "RAWDA-",
                 "(?i)^g-": "GAN-",
                 "(?i)RAWDA-E-1":"RAWDA-E",
                 "\([^)]+\)":"",
                 "(?i)ABRAR S-": "ABRAR- S-"
           
                   }
                 
                 
            for key,value in d.items():
                df5["well_name5"].replace(key,value,regex=True,inplace=True)
            
            #remove leading and preceding whitespaces
            df5["well_name5"] = df5["well_name5"].str.replace(r"\s*\*\s*", "", regex=True)
            
                 
     
                 
                 
            
            '''joining the data frames & giving them ID no from sql data base'''     
            
            merged_df = pd.merge(df3, df2, left_on='well_name3', right_on='well_name2',how = 'left')
            
            merged_df = pd.merge(merged_df, df1, left_on='well_name3', right_on='well_name1',how = 'left')
            
            merged_df = pd.merge(merged_df, df4, left_on='well_name3', right_on='well_name4',how = 'left')
            
            merged_df = pd.merge(merged_df, df5, left_on='well_name3', right_on='well_name5',how = 'left')
            
            merged_df['pump_intake'] = merged_df['pi_x'].fillna(merged_df['pi_y'])
            
            
            
            
            '''inserting date column extracted from the file name'''
            
            sheet_date = dparser.parse(infile,fuzzy=True, dayfirst=True).strftime("%Y-%m-%d")
            
            merged_df.insert(0, "date", sheet_date)
            
            dh.append(merged_df)
            
            print('{} done'.format(sheet_date))
            ''' concatinating the dataframes from all sheets and export as csv'''
            
dh=pd.concat(dh) 
       
dh.to_csv("mydata.csv")
            
print('finished safely')