import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data hasil clustering
df = pd.read_excel("hasil clustering kmeans.xlsx")

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
