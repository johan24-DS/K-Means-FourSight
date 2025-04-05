import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("AB_NYC_2019.csv")  # pastikan file ini tersedia
    df = df[['bedrooms', 'bathrooms', 'review_scores_rating']].dropna()
    return df

df = load_data()

# Preprocessing
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# Jalankan KMeans
kmeans = KMeans(n_clusters=5, random_state=42)
labels = kmeans.fit_predict(scaled_data)

# PCA untuk visualisasi
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

# Siapkan data untuk plotting
df_clustered = pd.DataFrame(pca_data, columns=["PC1", "PC2"])
df_clustered["Cluster"] = labels

# Streamlit UI
st.title("KMeans Airbnb Clustering Explorer")

# Input user
st.sidebar.header("🎯 Filter preferensi")
bedrooms = st.sidebar.slider("Jumlah kamar tidur", 0, 10, 1)
bathrooms = st.sidebar.slider("Jumlah kamar mandi", 0, 10, 1)
min_review, max_review = st.sidebar.slider("Range skor review", 0.0, 100.0, (50.0, 100.0))

# Transformasi input user ke PCA space
user_input = scaler.transform([[bedrooms, bathrooms, (min_review + max_review) / 2]])
user_pca = pca.transform(user_input)

# Prediksi cluster user
closest, _ = pairwise_distances_argmin_min(user_input, scaled_data)
user_cluster = labels[closest[0]]

# Visualisasi hasil clustering
st.subheader("Visualisasi Clustering (PCA)")
fig, ax = plt.subplots()
sns.scatterplot(x="PC1", y="PC2", hue="Cluster", data=df_clustered, palette="tab10", ax=ax)
ax.scatter(user_pca[0, 0], user_pca[0, 1], color='black', s=120, label="Input Anda", marker='X')
ax.legend()
st.pyplot(fig)

# Tampilkan hasil prediksi cluster
st.success(f"Input Anda diprediksi termasuk dalam Cluster: {user_cluster}")
