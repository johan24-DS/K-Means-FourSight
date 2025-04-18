import os
import streamlit as st
import pandas as pd

# Load data hasil clustering
df = pd.read_excel("Hasil Clustering KMeans.xlsx")

# Konversi kolom harga
df["price"] = df["price"].astype(str).str.replace("[$,]", "", regex=True)
df["price"] = pd.to_numeric(df["price"], errors='coerce')

# Mapping angka cluster ke nama unik
cluster_names = {
    1: "\ud83c\udfe0 Budget Single",
    2: "\ud83c\udfe1 Spacious Family Home",
    3: "\ud83c\udf1f Luxury Group Stay",
    4: "\ud83d\udebc Economy Shared Room",
    5: "\ud83d\udece\ufe0f Mid-Range Private Room"
}
df["cluster_name"] = df["cluster"].map(cluster_names)

# Streamlit UI config
st.set_page_config(page_title="Airbnb Recommendation System", layout="wide")

# Custom Traveloka-style CSS
st.markdown("""
    <style>
        body {
            background-color: #F5F8FA;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3, h4 {
            color: #2196F3;
        }

        .property-card {
            background-color: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
            transition: transform 0.2s;
        }

        .property-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        }

        .stButton>button {
            background-color: #2196F3;
            color: white;
            font-weight: bold;
            padding: 10px 24px;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #1976D2;
        }

        .filter-box {
            background-color: white;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1 style='text-align: center;'>\ud83c\udfe1 Airbnb Recommendation System</h1>", unsafe_allow_html=True)

# Logo
st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <img src="https://github.com/johan24-DS/K-Means-FourSight/raw/main/logo_foursight.jpg" width="300" />
        <p style="color: grey; font-size: 12px;">Created by : Foursight</p>
    </div>
""", unsafe_allow_html=True)

# FILTER SECTION
st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
st.subheader("\ud83d\udd0d Find your perfect Airbnb property")

col_top1, col_top2, col_top3 = st.columns(3)
with col_top1:
    cluster_option = st.multiselect("Select Cluster", options=sorted(df["cluster_name"].unique()), default=[])

# Filter data berdasarkan cluster yang dipilih
df_filtered_cluster = df[df["cluster_name"].isin(cluster_option)] if cluster_option else df

with col_top2:
    city_option = st.selectbox("Select City", ["All"] + sorted(df_filtered_cluster["city"].dropna().unique()))
with col_top3:
    street_option = st.selectbox("Select Street", ["All"] + sorted(df_filtered_cluster["street"].dropna().unique()))

col1, col2, col3, col4 = st.columns(4)
with col1:
    price_range = st.slider("\ud83d\udcb0 Price Range", int(df_filtered_cluster["price"].min()), int(df_filtered_cluster["price"].max()), (50, 250))
with col2:
    rating_range = st.slider("\u2b50 Review Scores", int(df_filtered_cluster["review_scores_rating"].min()), int(df_filtered_cluster["review_scores_rating"].max()), (80, 100))
with col3:
    num_bedrooms = st.number_input("\ud83d\udecf\ufe0f Min Bedrooms", min_value=0, max_value=int(df_filtered_cluster["bedrooms"].max()), value=1)
with col4:
    num_bathrooms = st.number_input("\ud83d\udebd Min Bathrooms", min_value=0, max_value=int(df_filtered_cluster["bathrooms"].max()), value=1)

sort_col1, sort_col2 = st.columns(2)
with sort_col1:
    sort_price = st.selectbox("Sort by Price", ["No Sort", "\u2b06\ufe0f Highest", "\u2b07\ufe0f Lowest"])
with sort_col2:
    sort_rating = st.selectbox("Sort by Review Score", ["No Sort", "\u2b06\ufe0f Highest", "\u2b07\ufe0f Lowest"])

st.markdown("</div>", unsafe_allow_html=True)

# FILTERING DATA
filtered_df = df_filtered_cluster[
    (df_filtered_cluster["price"] >= price_range[0]) & (df_filtered_cluster["price"] <= price_range[1]) &
    (df_filtered_cluster["review_scores_rating"] >= rating_range[0]) & (df_filtered_cluster["review_scores_rating"] <= rating_range[1]) &
    (df_filtered_cluster["bedrooms"] >= num_bedrooms) &
    (df_filtered_cluster["bathrooms"] >= num_bathrooms)
]

if city_option != "All":
    filtered_df = filtered_df[filtered_df["city"] == city_option]
if street_option != "All":
    filtered_df = filtered_df[filtered_df["street"] == street_option]

# Sorting
sort_by = []
if sort_price == "\u2b06\ufe0f Highest":
    sort_by.append(("price", False))
elif sort_price == "\u2b07\ufe0f Lowest":
    sort_by.append(("price", True))
if sort_rating == "\u2b06\ufe0f Highest":
    sort_by.append(("review_scores_rating", False))
elif sort_rating == "\u2b07\ufe0f Lowest":
    sort_by.append(("review_scores_rating", True))

if sort_by:
    sort_cols = [x[0] for x in sort_by]
    sort_asc = [x[1] for x in sort_by]
    filtered_df = filtered_df.sort_values(by=sort_cols, ascending=sort_asc)

filtered_df = filtered_df.head(10)

# AVERAGE PRICE
if not filtered_df.empty:
    avg_filtered_price = filtered_df["price"].mean()
    st.markdown(
        f"""
        <div style='background-color:#E3F2FD; padding: 20px; border-radius: 10px; margin-top: 20px;'>
            <h2 style='color:#0D47A1; margin: 0;'>\ud83d\udca1 Average Price</h2>
            <p style='font-size: 24px; font-weight: bold; color:#222;'>${avg_filtered_price:,.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("No properties match the selected criteria.")

# PROPERTY DISPLAY
st.subheader(f"\ud83c\udfe2 {len(filtered_df)} Properties Matching Your Criteria")

placeholder_image = "https://github.com/johan24-DS/K-Means-FourSight/raw/main/no-image.jpg"
cols = st.columns(3)

for i, (_, row) in enumerate(filtered_df.iterrows()):
    with cols[i % 3]:
        with st.container():
            image_url = row["picture_url"] if pd.notna(row["picture_url"]) and row["picture_url"].strip() != "" else placeholder_image
            st.image(image_url, use_container_width=True)
            st.markdown("<div class='property-card'>", unsafe_allow_html=True)
            st.markdown(f"**{row['name']}**")
            st.write(f"\ud83d\udccd {row['street']}, {row['city']}")
            st.write(f"\ud83d\udcb0 Price: ${row['price']:.2f}")
            st.write(f"\ud83d\udecf\ufe0f Bedrooms: {row['bedrooms']} | \ud83d\udebd Bathrooms: {row['bathrooms']}")
            st.write(f"\u2b50 Rating: {row['review_scores_rating']}/100")
            st.write(f"\ud83c\udff7\ufe0f Room Type: {row['room_type']}")
            st.markdown("</div>", unsafe_allow_html=True)
