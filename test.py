import os
...

# =============================
# 🏠 TAMPILKAN PROPERTY
# =============================
st.subheader(f"🏘️ {len(filtered_df)} Properties Matching Your Criteria")

cols = st.columns(3)

# Pastikan path placeholder sesuai dengan lokasi file Streamlit
placeholder_image = os.path.join(os.getcwd(), "No-Image.jpg")

for i, (_, row) in enumerate(filtered_df.iterrows()):
    with cols[i % 3]:
        with st.container():
            st.markdown('<div class="property-card">', unsafe_allow_html=True)
            
            # Logika fallback gambar
            image_url = row["picture_url"]
            if pd.isna(image_url) or image_url.strip() == "":
                st.image(placeholder_image, use_container_width=True)
            else:
                try:
                    st.image(image_url, use_container_width=True)
                except:
                    st.image(placeholder_image, use_container_width=True)

            # Konten property lainnya
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
