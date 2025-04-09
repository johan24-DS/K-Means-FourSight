import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data hasil clustering
df = pd.read_excel("Hasil Clustering KMeans.xlsx")

# Konversi kolom harga
df["price"] = df["price"].astype(str).str.replace("[$,]", "", regex=True)
df["price"] = pd.to_numeric(df["price"], errors='coerce')

# Mapping angka cluster ke nama unik
cluster_names = {
    1: "🏠 Budget Single",
    2: "🏡 Spacious Family Home",
    3: "🌟 Luxury Group Stay",
    4: "💼 Economy Shared Room",
    5: "🛏️ Mid-Range Private Room"
}
df["cluster_name"] = df["cluster"].map(cluster_names)

# Streamlit UI config
st.set_page_config(page_title="Airbnb Recommendation System", layout="wide")

# Custom CSS untuk styling kartu properti
st.markdown("""
    <style>
        .property-card {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
            margin-bottom: 20px;
            transition: 0.3s;
            height: 100%;
        }
        .property-card:hover {
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            transform: translateY(-4px);
        }
        .property-title {
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0 5px;
        }
        .property-text {
            font-size: 14px;
            margin-bottom: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# =============================
# 🔷 HEADER
# =============================
st.markdown("<h1 style='text-align: center;'>🏡 Airbnb Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Find your perfect Airbnb property based on your preferences!</h4>", unsafe_allow_html=True)

center_logo = st.columns([1, 2, 1])
with center_logo[1]:
    st.image("Logo Kelompok Foursight .jpg", width=200, caption="Created by : Foursight")

# =============================
# 🔍 FILTER SECTION
# =============================
st.subheader("🔎 Filter Your Search")

if st.checkbox("Show raw data"):
    st.write(df.head())

# Kolom untuk filter cluster, kota dan jalan
col_top1, col_top2, col_top3 = st.columns(3)
with col_top1:
    cluster_option = st.selectbox("Select Cluster", sorted(df["cluster_name"].unique()))
with col_top2:
    city_option = st.selectbox("Select City", ["All"] + sorted(df["city"].dropna().unique()))
with col_top3:
    street_option = st.selectbox("Select Street", ["All"] + sorted(df["street"].dropna().unique()))

# Kolom filter lanjutan
col1, col2, col3, col4 = st.columns(4)
with col1:
    price_range = st.slider("💰 Price Range", int(df["price"].min()), int(df["price"].max()),_
