import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load dataset
csv_path = os.path.join('dataset','HomeMatch_Kenya_Housing.csv')
df = pd.read_csv(csv_path)

st.title('📊 HomeMatch Dashboard')

# KPIs
st.header('Key Metrics')
col1, col2, col3 = st.columns(3)
col1.metric('Active Listings', len(df))
col2.metric('Average Rent', int(df['price'].mean()))
col3.metric('Occupancy Rate', f"{df['availability'].mean()*100:.1f}%" if 'availability' in df.columns else 'N/A')

# Distribution of prices
st.header('Rent Price Distribution')
fig, ax = plt.subplots()
sns.histplot(df['price'], kde=True, ax=ax)
st.pyplot(fig)

# Average rent by bedrooms
st.header('Average Rent by Bedrooms')
avg_by_beds = df.groupby('bedrooms')['price'].mean()
fig2, ax2 = plt.subplots()
avg_by_beds.plot(kind='bar', ax=ax2, title='Average Rent by Bedrooms')
st.pyplot(fig2)

# Scatter plot
st.header('Price vs. Bathrooms')
fig3, ax3 = plt.subplots()
sns.scatterplot(x='bathrooms', y='price', data=df, ax=ax3)
st.pyplot(fig3)
