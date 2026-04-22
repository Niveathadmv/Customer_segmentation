import pandas as pd
import numpy as np 


df = pd.read_excel(r'data/sales_data.xlsx')
## Fixing missing partyname
def missing_party_name_fix(df):

    condition= (
                df['BillType'].notna() & 
                df['Party Name @ Item'].isna()
    )
    df.loc[condition,'Party Name @ Item'] = 'Unknown'

    return df

df = missing_party_name_fix(df)
#---------------
def process_sales_data(df, bill_type_filter):

    result=[]
    current_bill_date = None
    current_bill_type = None
    current_party_name = None
## To fetch billtype, bill_date and partyname row by row
    for _,row in df.iterrows():

        if pd.notna(row['BillType']):
            current_bill_type = row['BillType']

            if current_bill_type == bill_type_filter:
                
                current_party_name = str(row['Party Name @ Item']).strip()
                
                if isinstance(row['Bill No @ Date'],str) and '@' in row['Bill No @ Date']:
                    current_bill_date = row['Bill No @ Date'].split('@')[1].strip()
                else:
                   current_bill_date = row['Bill No @ Date']
                    
            else:
                
                current_party_name= None
                current_bill_date= None
    
        if current_bill_type == bill_type_filter and pd.notna(row['Party Name @ Item']) and pd.notna(row['Qty']):
            
            result.append({
                'bill_date' : current_bill_date,
                'party_name': current_party_name,
                'item': row['Party Name @ Item'],
                'quantity': row['Qty'],
                'net_amount': row['Net Amt'],
                'rate': row['Rate']})
   
    return pd.DataFrame(result)
    
    


df1 = process_sales_data(df,'XXX')
df2 = process_sales_data(df,'YYY')

# Datatype and format cleaning
def datecol_cleaning(df,col):
    df = df[df[col].notna()]
    df[col] = pd.to_datetime(df[col],dayfirst=True, errors= 'coerce')

    return df

def numeric_col_cleaning(df,col):
   df[col] = pd.to_numeric(df[col].str.replace(',',''), errors= 'coerce')
   df[col] = df[col].fillna(0)
   #print(df.head())
   return df
#--------------------


#Combining 2 datasets
df1['Flag'] = 'XXX'
df2['Flag'] = 'YYY'

final_df = pd.concat([df1,df2])
final_df = numeric_col_cleaning(final_df,'net_amount')
final_df = datecol_cleaning(final_df,'bill_date')
#print(final_df.head())
final_df.to_excel(r'Cleaned_data.xlsx', index= False)

