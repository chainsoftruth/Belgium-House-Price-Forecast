# dashboard.py
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Belgium Properties Search", layout="wide")
st.title("🏠 Belgium Property Search")

# API endpoint
API_URL = "https://belgium-house-price-forecast-2.onrender.com/api/properties"

# Sidebar: filtreler
st.sidebar.header("Filters")
property_type = st.sidebar.selectbox("Property Type", ["All", "house", "apartment"])
postcode = st.sidebar.text_input("Postcode (optional)")
price_min = st.sidebar.number_input("Min Price", value=0, step=10000)
price_max = st.sidebar.number_input("Max Price", value=1000000, step=10000)

# Search butonu
if st.sidebar.button("Search"):
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        # Eğer API boş liste dönerse demo veri kullan
        if not data:
            st.warning("API veri döndürmedi, demo verisi gösteriliyor.")
            df = pd.DataFrame([
                {"Post code": "1000", "Type of property": "house", "Price": 300000, "Living Area": 120},
                {"Post code": "1050", "Type of property": "apartment", "Price": 200000, "Living Area": 80},
                {"Post code": "1030", "Type of property": "house", "Price": 450000, "Living Area": 180},
            ])
        else:
            df = pd.DataFrame(data)
    except Exception as e:
        st.error(f"API'den veri çekilemedi: {e}")
        # Hata olsa bile demo veri göster
        df = pd.DataFrame([
            {"Post code": "1000", "Type of property": "house", "Price": 300000, "Living Area": 120},
            {"Post code": "1050", "Type of property": "apartment", "Price": 200000, "Living Area": 80},
            {"Post code": "1030", "Type of property": "house", "Price": 450000, "Living Area": 180},
        ])

    # Filtreleme
    if property_type != "All":
        df = df[df["Type of property"] == property_type]
    if postcode:
        df = df[df["Post code"] == postcode]
    df = df[(df["Price"] >= price_min) & (df["Price"] <= price_max)]

    st.subheader(f"Search Results ({len(df)} properties)")
    st.dataframe(df)

    if not df.empty:
        st.subheader("Price Distribution")
        st.bar_chart(df["Price"])

        if "Living Area" in df.columns:
            st.subheader("Living Area Distribution")
            st.bar_chart(df["Living Area"])
    else:
        st.write("No properties found with these filters.")