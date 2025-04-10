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

for i, (_, row) in enumerate(filtered_df.iterrows()):
    with cols[i % 3]:
        with st.container():
            st.markdown('<div class="property-card">', unsafe_allow_html=True)

            # ✅ Gambar fallback jika kosong
            if pd.isna(row["picture_url"]) or row["picture_url"] == "":
                st.image("https://via.placeholder.com/400x300?text=No+Image", use_container_width=True)
            else:
                st.image(row["picture_url"], use_container_width=True)

            # ✅ Tambahkan nomor urut
            st.markdown(
                f'<div class="property-title">{i+1}. <a href="{row["listing_url"]}" target="_blank">{row["name"]}</a></div>',
                unsafe_allow_html=True
            )
            st.markdown(f'<div class="property-text">📍 <b>{row["street"]}, {row["city"]}</b></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="property-text">💰 Price: ${row["price"]:.2f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="property-text">🛏️ Bedrooms: {row["bedrooms"]} | 🛁 Bathrooms: {row["bathrooms"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="property-text">⭐ Rating: {row["review_scores_rating"]}/100</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="property-text">🏷️ Room Type: {row["room_type"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
