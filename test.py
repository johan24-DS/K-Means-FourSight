import os
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

# ================================
# 💅 Custom CSS Styling
# ================================
st.markdown("""
    <style>
        .grid-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: flex-start;
        }
        .grid-item {
            flex: 1 1 calc(33.333% - 20px);
            box-sizing: border-box;
        }
        @media (max-width: 768px) {
            .grid-item {
                flex: 1 1 calc(50% - 20px);
            }
        }
        @media (max-width: 480px) {
            .grid-item {
                flex: 1 1 100%;
            }
        }
        .property-card {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
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

# ================================
# 🔷 HEADER
# ================================
st.markdown("<h1 style='text-align: center;'>🏡 Airbnb Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Find your perfect Airbnb property with FourSight!</h4>", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <img src="https://github.com/johan24-DS/K-Means-FourSight/raw/main/logo_foursight.jpg" width="300" />
        <p style="color: grey; font-size: 12px;">Created by : Foursight</p>
    </div>
""", unsafe_allow_html=True)

# ================================
# 🔍 FILTER SECTION
# ================================
st.subheader("🔎 Find your perfect Airbnb property")

# Cluster filter terlebih dahulu
col_top1, col_top2, col_top3 = st.columns(3)
with col_top1:
    cluster_option = st.multiselect(
        "Select Cluster(s)",
        options=sorted(df["cluster_name"].unique()),
        default=sorted(df["cluster_name"].unique())
    )

# Filter dataframe sementara berdasarkan cluster
filtered_cluster_df = df[df["cluster_name"].isin(cluster_option)]

# City & Street menyesuaikan cluster
with col_top2:
    city_option = st.selectbox(
        "Select City",
        ["All"] + sorted(filtered_cluster_df["city"].dropna().unique())
    )

with col_top3:
    if city_option != "All":
        street_choices = filtered_cluster_df[filtered_cluster_df["city"] == city_option]["street"].dropna().unique()
    else:
        street_choices = filtered_cluster_df["street"].dropna().unique()

    street_option = st.selectbox(
        "Select Street",
        ["All"] + sorted(street_choices)
    )

# Filter lanjutan
col1, col2, col3, col4 = st.columns(4)
with col1:
    price_range = st.slider("💰 Price Range", int(df["price"].min()), int(df["price"].max()), (50, 250))
with col2:
    rating_range = st.slider("⭐ Review Scores", int(df["review_scores_rating"].min()),
                             int(df["review_scores_rating"].max()), (80, 100))
with col3:
    num_bedrooms = st.number_input("🛏️ Min Bedrooms", min_value=0, max_value=int(df["bedrooms"].max()), value=1)
with col4:
    num_bathrooms = st.number_input("🛁 Min Bathrooms", min_value=0, max_value=int(df["bathrooms"].max()), value=1)

# Sorting
sort_col1, sort_col2 = st.columns(2)
with sort_col1:
    sort_price = st.selectbox("Sort by Price", ["No Sort", "⬆️ Highest", "⬇️ Lowest"])
with sort_col2:
    sort_rating = st.selectbox("Sort by Review Score", ["No Sort", "⬆️ Highest", "⬇️ Lowest"])

# ================================
# 🧮 FINAL FILTERING
# ================================
filtered_df = filtered_cluster_df[
    (filtered_cluster_df["price"] >= price_range[0]) &
    (filtered_cluster_df["price"] <= price_range[1]) &
    (filtered_cluster_df["review_scores_rating"] >= rating_range[0]) &
    (filtered_cluster_df["review_scores_rating"] <= rating_range[1]) &
    (
