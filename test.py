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
    # Filter berdasarkan cluster terlebih dahulu
cluster_option = st.multiselect(
    "Select Cluster(s)",
    options=sorted(df["cluster_name"].unique()),
    default=sorted(df["cluster_name"].unique())
)

# Data sementara hanya berdasarkan cluster
filtered_cluster_df = df[df["cluster_name"].isin(cluster_option)]

# Filter dropdown City & Street berdasarkan cluster yang dipilih
with col_top2:
    city_option = st.selectbox(
        "Select City",
        ["All"] + sorted(filtered_cluster_df["city"].dropna().unique())
    )

with col_top3:
    # Filter street berdasarkan city (jika dipilih)
    if city_option != "All":
        street_choices = filtered_cluster_df[filtered_cluster_df["city"] == city_option]["street"].dropna().unique()
    else:
        street_choices = filtered_cluster_df["street"].dropna().unique()
        
    street_option = st.selectbox(
        "Select Street",
        ["All"] + sorted(street_choices)
    )


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
filtered_df = filtered_cluster_df[
    (filtered_cluster_df["price"] >= price_range[0]) & 
    (filtered_cluster_df["price"] <= price_range[1]) &
    (filtered_cluster_df["review_scores_rating"] >= rating_range[0]) & 
    (filtered_cluster_df["review_scores_rating"] <= rating_range[1]) &
    (filtered_cluster_df["bedrooms"] >= num_bedrooms) &
    (filtered_cluster_df["bathrooms"] >= num_bathrooms)
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
# 💰 TAMPILKAN RATA-RATA HARGA
# =============================
if not filtered_df.empty:
    avg_filtered_price = filtered_df["price"].mean()
    st.markdown(f"💡 **Average price of filtered properties:** `${avg_filtered_price:,.2f}`")
else:
    st.warning("No properties match the selected criteria.")


# =============================
# 🏠 TAMPILKAN PROPERTY
# =============================
st.subheader(f"🏘️ {len(filtered_df)} Properties Matching Your Criteria")

# URL fallback untuk gambar placeholder
placeholder_image = "https://github.com/johan24-DS/K-Means-FourSight/raw/main/no-image.jpg"

# Buat 3 kolom tetap
cols = st.columns(3)

# Loop hasil properti
for i, (_, row) in enumerate(filtered_df.iterrows()):
    with cols[i % 3]:  # simpan ke kolom 0, 1, 2 lalu ulang
        with st.container(border=True):
            # Gambar
            image_url = row["picture_url"]
            if pd.isna(image_url) or image_url.strip() == "":
                st.image(placeholder_image, use_container_width=True)
            else:
                try:
                    st.image(image_url, use_container_width=True)
                except:
                    st.image(placeholder_image, use_container_width=True)

            # Info Properti
            st.markdown(f"**{i+1}. [{row['name']}]({row['listing_url']})**")
            st.write(f"📍 {row['street']}, {row['city']}")
            st.write(f"💰 Price: ${row['price']:.2f}")
            st.write(f"🛏️ Bedrooms: {row['bedrooms']} | 🛁 Bathrooms: {row['bathrooms']}")
            st.write(f"⭐ Rating: {row['review_scores_rating']}/100")
            st.write(f"🏷️ Room Type: {row['room_type']}")

