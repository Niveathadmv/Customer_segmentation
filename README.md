# Customer_segmentation
Customer Segmentation — Small Scale B2B Business
**##**

**Problem**

A small scale business was heavily dependent on a single 
high-volume customer (X). While this customer contributed 
significantly to revenue, their payments were consistently 
delayed — affecting the company's ability to purchase raw 
materials on time.

The business didn't have visibility into:
- Who their other valuable customers were
- Which customers had growth potential
- Whether it was worth continuing to prioritize customer X
  or gradually diversify their customer base

**##**

**Dataset**

Real transactional sales data from the business.
Not attached for privacy reasons.
Contains order-level data with billing dates, party names,
and net amounts across 90 customers.

**##**

**Approach**

**Step 1 — Data Cleaning**

Raw transactional data was cleaned before analysis:

- Handled missing values
- Standardized date formats
- Removed duplicates
- Parsed and flattened a hierarchical row structure — bill metadata (bill number, date, party name) and item-level details (item name, quantity, rate, amount) were stored in merged/nested rows in the source Excel.
- Restructured into a flat, analysis-ready format with each row representing one line item per bill.

Before:

<img width="1338" height="162" alt="Screenshot 2026-04-22 122047" src="https://github.com/user-attachments/assets/255d9954-361b-40fa-962c-ead3167c3b70" />

After:

<img width="1089" height="98" alt="Screenshot 2026-04-22 122145" src="https://github.com/user-attachments/assets/58fca9cf-816e-455d-a2c0-64b6b39790bc" />


**###**

**Step 2 — RFM Rule-Based Segmentation**

Customers scored on Recency, Frequency and Monetary values and segmented using business logic thresholds.
Produced 8 meaningful segments with better granularity given the dataset size.

**###**

**Step 3 — RFM + KMeans Clustering**

StandardScaler + KMeans (K=5) applied on RFM features.
Elbow method and Silhouette score used to choose K.
With 90 customers, clustering produced broad groups.
Results validate the rule-based approach rather than replace it.

**###**

**Why both?**

Dataset has 90 customers. Clustering works best with larger data.
Rule-based RFM gave more actionable segments for the client.
Clustering is included to demonstrate the methodology and will produce sharper results as the business grows and data scales.
**##**

**Results**

**Clustering output**
<img width="881" height="531" alt="image" src="https://github.com/user-attachments/assets/db6310e9-a58d-4000-8f46-6b80a1905d8c" />

**RFM output**
<img width="890" height="533" alt="image" src="https://github.com/user-attachments/assets/92d0cebd-f97e-4a1c-b39a-891e3027458e" />

**RFM customer count**
Low valued customers     	26
Hibernating              	14
Loyal                    	12
Most valued customers    	12
Needs attention          	10
Potential                	10
At risk                   4
New customers             4

Customer X was identified within the Most Valued Customers
segment- highest frequency and monetary contribution.
But, given the payment delay risk, over-dependence on this segment is a business vulnerability.

**##**

**Business Insights**

**1. Don't build on one pillar**
- Customer X is valuable but risky. Delayed payments directly impact cash flow and material procurement. 
The data confirms this is a single point of failure for the business.

**2. Loyal customers are the real opportunity**
- 12 customers sit in the Loyal segment, they're consistent buyers with good frequency. 
These are the safest candidates to nurture and grow. Low effort but high trust already been established.

**3. Potential customers need attention now**
- 10 customers are classified as Potential. They are buying but not yet frequently. 
A small push like better service, priority delivery, relationship building could move them into Loyal or Most Valued over time.

**4. Gradual diversification strategy**
Rather than dropping customer X abruptly, the business can:
- Slowly increase capacity allocation to Loyal and Potential
- Set clearer payment terms with customer X
- Track if new customers move up segments over 6 months
