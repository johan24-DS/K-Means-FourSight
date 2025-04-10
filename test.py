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

# Custom CSS untuk styling kartu properti
# Tambahkan ini ke bagian CSS kamu
# Tambahkan CSS untuk konsistensi ukuran gambar dan kontainer
st.markdown("""
    <style>
    .property-card {
        background-color: #fff;
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 16px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .property-image img {
        object-fit: cover;
        width: 100%;
        height: 200px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)



# =============================
# 🔷 HEADER
# =============================
st.markdown("<h1 style='text-align: center;'>🏡 Airbnb Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Find your perfect Airbnb property with FourSight!</h4>", unsafe_allow_html=True) 

# 🖼️ Logo benar-benar di tengah dengan HTML
st.markdown(
    """
    <div style="text-align: center; margin-top: 30px;">
        <img src="https://github.com/johan24-DS/K-Means-FourSight/raw/main/logo_foursight.jpg" width="300" />
        <p style="color: grey; font-size: 12px;">Created by : Foursight</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =============================
# 🔍 FILTER SECTION
# =============================
st.subheader("🔎 Find your perfect Airbnb property") 

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

# =============================
# 🧮 FILTERING DATA
# =============================
filtered_df = df[
    (df["cluster_name"] == cluster_option) &
    (df["price"] >= price_range[0]) & (df["price"] <= price_range[1]) &
    (df["review_scores_rating"] >= rating_range[0]) & (df["review_scores_rating"] <= rating_range[1]) &
    (df["bedrooms"] >= num_bedrooms) &
    (df["bathrooms"] >= num_bathrooms)
]

if city_option != "All":
    filtered_df = filtered_df[filtered_df["city"] == city_option]

if street_option != "All":
    filtered_df = filtered_df[filtered_df["street"] == street_option]

# Sorting
sort_by = []
if sort_price == "⬆️ Highest":
    sort_by.append(("price", False))
elif sort_price == "⬇️ Lowest":
    sort_by.append(("price", True))

if sort_rating == "⬆️ Highest":
    sort_by.append(("review_scores_rating", False))
elif sort_rating == "⬇️ Lowest":
    sort_by.append(("review_scores_rating", True))

if sort_by:
    sort_cols = [x[0] for x in sort_by]
    sort_asc = [x[1] for x in sort_by]
    filtered_df = filtered_df.sort_values(by=sort_cols, ascending=sort_asc)

filtered_df = filtered_df.head(10)

# =============================
# 🏠 TAMPILKAN PROPERTY
# =============================
st.subheader(f"🏘️ {len(filtered_df)} Properties Matching Your Criteria")

cols = st.columns(3)
placeholder_image = "https://github.com/johan24-DS/K-Means-FourSight/raw/main/no-image.jpg"

for i, (_, row) in enumerate(filtered_df.iterrows()):
    with cols[i % 3]:
        with st.container():
            st.markdown('<div class="property-card">', unsafe_allow_html=True)

            # Gambar
            image_url = row["picture_url"]
            if pd.isna(image_url) or image_url.strip() == "":
                img = placeholder_image
            else:
                img = image_url

            # Tampilkan gambar dengan div agar CSS-nya aktif
            st.markdown(f'<div class="property-image"><img src="{img}" alt="Property Image"></div>', unsafe_allow_html=True)

            # Informasi properti
            st.markdown(f"**{i+1}. [{row['name']}]({row['listing_url']})**")
            st.write(f"📍 {row['street']}, {row['city']}")
            st.write(f"💰 Price: ${row['price']:.2f}")
            st.write(f"🛏️ Bedrooms: {row['bedrooms']} | 🛁 Bathrooms: {row['bathrooms']}")
            st.write(f"⭐ Rating: {row['review_scores_rating']}/100")
            st.write(f"🏷️ Room Type: {row['room_type']}")
            st.markdown('</div>', unsafe_allow_html=True)
