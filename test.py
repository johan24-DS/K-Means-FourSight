import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data hasil clustering
df = pd.read_excel("Hasil Clustering KMeans.xlsx")

# Streamlit UI
st.set_page_config(page_title="Airbnb Recommendation System", layout="wide")
st.title("🏡 Airbnb Recommendation System")
st.subheader("Find your perfect Airbnb property based on your preferences!")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("Logo Kelompok Foursight .jpg", caption="Created by : Foursight", width=200)

# Checkbox untuk menampilkan data mentah
if st.checkbox("Show raw data"):
    st.write(df.head())

# Mapping angka cluster ke nama unik
cluster_names = {
    1: "🏠 Budget Single",
    2: "🏡 Spacious Family Home",
    3: "🌟 Luxury Group Stay",
    4: "💼 Economy Shared Room",
    5: "🛏️ Mid-Range Private Room"
}
df["cluster_name"] = df["cluster"].map(cluster_names)

# Konversi kolom harga
df["price"] = df["price"].astype(str).str.replace("[$,]", "", regex=True)
df["price"] = pd.to_numeric(df["price"], errors='coerce')

# Dropdown untuk memilih cluster tertentu
cluster_option = st.selectbox("Select Cluster", sorted(df["cluster_name"].unique()))

# Filter input
col1, col2, col3, col4 = st.columns(4)
with col1:
    price_range = st.slider("Price Range", int(df["price"].min()), int(df["price"].max()), (50, 250))
with col2:
    rating_range = st.slider("Review Scores", int(df["review_scores_rating"].min()),
                             int(df["review_scores_rating"].max()), (80, 100))
with col3:
    num_bedrooms = st.number_input("Min Bedrooms", min_value=0, max_value=int(df["bedrooms"].max()), value=1, step=1)
with col4:
    num_bathrooms = st.number_input("Min Bathrooms", min_value=0, max_value=int(df["bathrooms"].max()), value=1, step=1)

# Filter data
filtered_df = df[
    (df["cluster_name"] == cluster_option) &
    (df["price"] >= price_range[0]) & (df["price"] <= price_range[1]) &
    (df["review_scores_rating"] >= rating_range[0]) & (df["review_scores_rating"] <= rating_range[1]) &
    (df["bedrooms"] >= num_bedrooms) &
    (df["bathrooms"] >= num_bathrooms)
]

# Tampilkan listing properti dalam grid
st.subheader(f"🏘️ {len(filtered_df)} Properties Matching Your Criteria")

# Layout grid (3 properti per baris)
cols = st.columns(3)

for i, (_, row) in enumerate(filtered_df.iterrows()):
    with cols[i % 3]:
        with st.container():
            st.image(row["picture_url"], use_container_width=True)
            st.markdown(f"#### [{row['name']}]({row['listing_url']})", unsafe_allow_html=True)
            st.markdown(f"📍 **{row['street']}, {row['city']}**", unsafe_allow_html=True)
            st.markdown(f"💰 **Price:** ${row['price']:.2f}")
            st.markdown(f"🛏️ **Bedrooms:** {row['bedrooms']} | 🛁 **Bathrooms:** {row['bathrooms']}")
            st.markdown(f"⭐ **Rating:** {row['review_scores_rating']}/100")
            st.markdown(f"🏷️ **Room Type:** {row['room_type']}")

# Scatter Plot
st.subheader("📊 Price vs. Review Scores Rating (Clustered)")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="price",
    y="review_scores_rating",
    hue="cluster_name",
    palette="Set2",
    ax=ax
)
ax.set_xlabel("Price")
ax.set_ylabel("Review Scores Rating")
st.pyplot(fig)

# Pie Chart
st.subheader("🏠 Room Type Distribution in Selected Cluster")
fig, ax = plt.subplots()
filtered_df["room_type"].value_counts().plot.pie(
    autopct="%1.1f%%",
    startangle=140,
    cmap="Set2",
    ax=ax
)
ax.set_ylabel("")  # remove default ylabel
st.pyplot(fig)
