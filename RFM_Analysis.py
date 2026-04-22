import pandas as pd
import numpy as np
import regex as re
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_excel(r'cleaned_data.xlsx')

#RFM
def rfm_calculation(df):

    reference_date = df['bill_date'].max()
    rfm = df.groupby('party_name').agg({
        'bill_date': [lambda bill_date: (reference_date - bill_date.max()).days, 'count'],
        #'bill_date': 'count',
        'net_amount' : 'sum'
    })
    return rfm

rfm = rfm_calculation(df)

rfm.columns = ['recency', 'frequency','monetary']
rfm = rfm.reset_index()

#RFM score
def rfm_scores_segments(df):
    rfm['r_score'] = pd.qcut(rfm['recency'],5, labels= [5,4,3,2,1])
    rfm['f_score'] = pd.qcut(rfm['frequency'], 5, labels=[1,2,3,4,5])
    rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])

    rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)

    # RFM segments- using only R anf F score to avoid too many segments
    """
    def rfm_segments(row):
            if row['r_score'] >= 4 and row['f_score'] >= 4:
                return 'Most valued customers'
            elif row['r_score'] >= 3 and row['f_score'] >= 3:
                return 'Loyal customers'
            elif row['r_score'] >= 4 and row['f_score'] <=2:
                return 'New customers'
            elif row['r_score'] <= 2 and row['f_score'] >=3:
                return 'At risk'
            else:
                return 'Low value customers'*/
    """
    seg_map = {
        r'5[4-5]'    : 'Most valued customers',
        r'4[4-5]'    : 'Loyal',
        r'[4-5]1': 'New customers',
        r'[4-5][2-3]': 'Potential',
        r'[1-2][4-5]': 'At risk',
        r'3[3-5]'    : 'Needs attention',
        r'3[1-2]'    : 'Low valued customers',
        r'[1-2][2-3]': 'Low valued customers',
        r'[1-2][1]': 'Hibernating' 
    }

    rfm['segments'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str)
    rfm['segments'] = rfm['segments'].replace(seg_map, regex=True)
    return rfm

rfm = rfm_scores_segments(rfm)

#print(rfm['segments'].value_counts())

# Bar chart — segment wise customer count
plt.figure(figsize=(10, 6))
rfm_counts = rfm['segments'].value_counts().reset_index()
rfm_counts.columns = ['segments', 'count']

sns.barplot(data=rfm_counts, x='count', y='segment', palette='Set2')

plt.title('Customer Count by RFM Segment')
plt.xlabel('Number of Customers')
plt.ylabel('Segment')

plt.tight_layout()
plt.savefig('rfm_segments.png')
plt.show()

#rfm.to_excel(r'rfm.xlsx')

    


