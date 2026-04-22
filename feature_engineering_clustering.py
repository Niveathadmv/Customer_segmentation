import pandas as pd
import numpy as np
import regex as re
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
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

#--------------RFM ends---------------
##-----------clustering begins---------------
scaler = StandardScaler()
scaled_df = scaler.fit_transform(rfm[['recency', 'frequency', 'monetary']])

##Finding groups using Kmeans(Elbow method)

inertia = []
for i in range(1,10):
    kmeans = KMeans(n_clusters= i, random_state= 42)
    kmeans.fit(scaled_df)
    inertia.append(kmeans.inertia_)

plt.plot(range(1, 10), inertia, marker='o')
plt.xlabel('Number of clusters (K)')
plt.ylabel('Inertia')
plt.title('Elbow Method')
#plt.show()

## Validating using silhouette score
for i in range(2,10):
    kmeans = KMeans(n_clusters= i, random_state= 42)  # creates the clusters for K=i
    labels = kmeans.fit_predict(scaled_df)  # assign those learned clusters for each row
    score = silhouette_score(scaled_df, labels)  # grades the grouping decision says how well customers are separated
    #print(i,score)


## grouping customers with chosen clusters or i

kmeans_final = KMeans(n_clusters= 5, random_state= 42)

# fit_predict gives cluster labels for each row

labels_final = kmeans_final.fit_predict(scaled_df)

# assigning to original dataframe dataframe

rfm['clusters'] = labels_final


##-----------clustering ends---------------
##-----Interpretation------
#print(rfm.groupby('clusters')[['recency', 'frequency', 'monetary']].mean().round(2))

cluster_labels = {
    0 : 'At Risk',
    1 : 'Lost Customers',
    2 : 'Loyal Customers',
    3 : 'Most Valued Customers',
    4 : 'Potential Loyalists'
}

rfm['segments'] = rfm['clusters'].replace(cluster_labels, regex = True)

#print(rfm['segments'].value_counts())

# Scatter plot — Frequency vs Monetary colored by cluster
plt.figure(figsize=(10, 6))
sns.scatterplot(data=rfm, x='frequency', y='monetary', 
                hue='segments', palette='Set2', s=100)
plt.title('Customer Segments — KMeans Clustering')
plt.xlabel('Frequency')
plt.ylabel('Monetary')
plt.legend(title='Segment')
plt.tight_layout()
plt.savefig('cluster_visualization.png')
plt.show()


#rfm.to_excel(r'clustering_segments.xlsx')