import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load env variables
load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "Edwin@123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "homematch_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Custom CSS
st.markdown("""
    <style>
        .header {
            background-color: #008000;
            padding: 15px;
            text-align: center;
            color: white;
            font-size: 32px;
            font-weight: bold;
            border-radius: 5px;
        }
        .search-bar {
            margin: 20px auto;
            text-align: center;
        }
        .category-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .category {
            background-color: #008000;
            border: 1px solid #ddd;
            padding: 15px;
            margin: 5px;
            border-radius: 8px;
            text-align: center;
            width: 150px;
            cursor: pointer;
            transition: 0.3s;
        }
        .category:hover {
            background-color: #e6ffe6;
        }
        .results-header {
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 26px;
            font-weight: bold;
            text-align: center;
            color: #333;
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px;
            width: 300px;
            display: inline-block;
            vertical-align: top;
        }
        .card img {
            width: 100%;
            height: 180px;
            object-fit: cover;
        }
        .card-body {
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='header'>HomeMatch</div>", unsafe_allow_html=True)

# Search Bar
with st.form("search_form"):
    st.markdown("<div class='search-bar'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        city = st.text_input("Location (e.g. Nairobi)", "")
    with col2:
        keyword = st.text_input("I am looking for...", "")
    with col3:
        submitted = st.form_submit_button("Search 🔎")
    st.markdown("</div>", unsafe_allow_html=True)

# Categories
st.markdown("<div class='category-container'>", unsafe_allow_html=True)
for cat in ["Apartments", "Bedsitters", "Maisonettes", "Bungalows", "Offices", "Land"]:
    st.markdown(f"<div class='category'>{cat}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Results section
results = pd.DataFrame()
if submitted:
    query = "SELECT * FROM housing_data WHERE 1=1"
    params = {}
    if city:
        query += " AND city ILIKE :city"
        params["city"] = f"%{city}%"
    if keyword:
        query += " AND (location_name ILIKE :kw OR property_type ILIKE :kw OR amenities ILIKE :kw)"
        params["kw"] = f"%{keyword}%"

    with engine.connect() as conn:
        results = pd.read_sql(text(query + " LIMIT 30"), conn, params=params)

    # Results header
    st.markdown("<div class='results-header'>Results</div>", unsafe_allow_html=True)

# Show results
if not results.empty:
    for _, row in results.iterrows():
        st.markdown(f"""
        <div class="card">
            <img src="{row['image_url'] or 'https://via.placeholder.com/300x200'}">
            <div class="card-body">
                <h4>{row['location_name']} - {row['city']}</h4>
                <p>
                    🏷 {row['property_type']}<br>
                    🛏 {row['bedrooms']} BR | 🛁 {row['bathrooms']} BA<br>
                    💰 {row['price_ksh']:,} KSH<br>
                    🛠 {row['amenities'] or 'N/A'}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
