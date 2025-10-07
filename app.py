import streamlit as st, pandas as pd, os

st.set_page_config(page_title='HomeMatch', layout='wide')
st.markdown("<h1 style='text-align: center;'>🏡 HomeMatch</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>Used by Realtors, Landlords and Tenants</div>", unsafe_allow_html=True)

# Load dataset
CSV1 = 'HomeMatch_Kenya_Housing.csv'
CSV2 = os.path.join('dataset','HomeMatch_Kenya_Housing.csv')
csv_path = CSV1 if os.path.exists(CSV1) else CSV2

df = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame()

# Sidebar filters
st.sidebar.header('Filters')
st.sidebar.markdown('<div style="text-align: center;">Search By:</div>', unsafe_allow_html=True)

if not df.empty:
    # Price filter
    min_price, max_price = st.sidebar.slider(
        'Price (KSh)', 
        int(df['price'].min()), int(df['price'].max()), 
        (int(df['price'].min()), int(df['price'].max()))
    )
    # Bedrooms filter
    bedrooms = st.sidebar.selectbox('Bedrooms', sorted(df['bedrooms'].unique()))
    # Location name filter
    location_name = st.sidebar.text_input('Location Name (e.g. Kilimani)')
    # Longitude/Latitude filter
    longitude = st.sidebar.number_input('Longitude', value=0.0, format="%.6f")
    latitude = st.sidebar.number_input('Latitude', value=0.0, format="%.6f")
    # Amenities filter (comma-separated)
    amenities = st.sidebar.text_input("Amenities (comma-separated, e.g. wifi,parking)")
else:
    min_price,max_price,bedrooms,location_name,longitude,latitude,amenities = 0,0,0,"",0.0,0.0,""

# Tabs
tab1, tab2 = st.tabs(['Browse Homes','Saved Homes'])
if 'saved' not in st.session_state: 
    st.session_state['saved'] = []

with tab1:
    st.subheader('Browse Homes')
    if not df.empty:
        df_filtered = df[
            (df['price'] >= min_price) &
            (df['price'] <= max_price) &
            (df['bedrooms'] == bedrooms)
        ]
        # Location name filter
        if location_name:
            df_filtered = df_filtered[df_filtered['location_name'].str.contains(location_name, case=False, na=False)]
        # Longitude/Latitude filter (approx match within ±0.01)
        if longitude != 0.0:
            df_filtered = df_filtered[(df_filtered['longitude'].between(longitude-0.01, longitude+0.01))]
        if latitude != 0.0:
            df_filtered = df_filtered[(df_filtered['latitude'].between(latitude-0.01, latitude+0.01))]
        # Amenities filter
        if amenities:
            for a in amenities.split(","):
                a = a.strip().lower()
                df_filtered = df_filtered[df_filtered['amenities'].str.lower().str.contains(a, na=False)]

        if df_filtered.empty:
            st.info('No exact matches - showing recommendations...')
        else:
            for idx,row in df_filtered.iterrows():
                cols = st.columns([1,2])
                with cols[0]:
                    st.image(row.get('image_url','https://via.placeholder.com/150'), width=120)
                with cols[1]:
                    st.markdown(f"**{row.get('name','Listing')}** — KSh {row.get('price',0)}")
                    st.markdown(f"{row.get('bedrooms',0)} bd • {row.get('bathrooms',0)} ba • {row.get('location_name','')}")
                    if st.button('💾 Save Home', key=f'save{idx}'):
                        if idx not in st.session_state['saved']: 
                            st.session_state['saved'].append(idx)
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
