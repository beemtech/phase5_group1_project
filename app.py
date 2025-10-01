import streamlit as st, pandas as pd, os

st.set_page_config(page_title='HomeMatch', layout='wide')
st.title('🏡 HomeMatch — Demo (Final v3)')

CSV1 = 'HomeMatch_Kenya_Housing.csv'
CSV2 = os.path.join('dataset','HomeMatch_Kenya_Housing.csv')
csv_path = CSV1 if os.path.exists(CSV1) else CSV2

df = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame()

st.sidebar.header('Filters')
if not df.empty:
    min_price, max_price = st.sidebar.slider('Price (KSh)', int(df['price'].min()), int(df['price'].max()), (int(df['price'].min()), int(df['price'].max())))
    bedrooms = st.sidebar.selectbox('Bedrooms', sorted(df['bedrooms'].unique()))
else:
    min_price,max_price,bedrooms = 0,0,0

tab1, tab2 = st.tabs(['Browse Homes','Saved Homes'])
if 'saved' not in st.session_state: st.session_state['saved'] = []

with tab1:
    st.subheader('Browse Homes')
    if not df.empty:
        df_filtered = df[(df['price']>=min_price)&(df['price']<=max_price)&(df['bedrooms']==bedrooms)]
        if df_filtered.empty:
            st.info('No exact matches - showing recommendations...')
        else:
            for idx,row in df_filtered.iterrows():
                cols = st.columns([1,2])
                with cols[0]:
                    st.image(row.get('image_url','https://via.placeholder.com/150'), width=120)
                with cols[1]:
                    st.markdown(f"**{row.get('name','Listing')}** — KSh {row.get('price',0)}")
                    st.markdown(f"{row.get('bedrooms',0)} bd • {row.get('bathrooms',0)} ba")
                    if st.button('💾 Save Home', key=f'save{idx}'):
                        if idx not in st.session_state['saved']: st.session_state['saved'].append(idx)
                    st.markdown(f"[📩 Contact Owner](mailto:owner@example.com?subject=Listing%20{idx})")

with tab2:
    st.subheader('Saved Homes')
    if not st.session_state['saved']:
        st.info('No saved homes yet')
    else:
        for s in st.session_state['saved']:
            r = df.iloc[s]
            st.markdown(f"**{r.get('name','Listing')}** — KSh {r.get('price',0)}")
            st.image(r.get('image_url','https://via.placeholder.com/150'), width=180)
