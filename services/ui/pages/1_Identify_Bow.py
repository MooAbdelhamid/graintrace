import streamlit as st
from lib import api_client

st.title("Identify a bow")

photo = st.file_uploader("Upload a query photo", type=["jpg", "jpeg", "png"])

if photo and st.button("Verify", type="primary"):
    try:
        result = api_client.verify(photo.getvalue(), filename=photo.name)

        st.success("Query processed")

        # Show API response
        st.json(result)

        matches = result.get("matches", [])

        if matches:
            st.subheader("Matching bows")

            # Get top 3 matches
            for match in matches[:3]:
                bow_id = match["bow_id"]

                st.write(f"Bow ID: {bow_id}")
                st.write(f"Score: {match['score']}")

                try:
                    image_bytes = api_client.meta_image(bow_id)
                    st.image(image_bytes, caption=bow_id, width=300)

                except Exception as img_error:
                    st.warning(f"Could not load image for {bow_id}: {img_error}")

        else:
            st.info("No matching bows found")

    except Exception as e:
        st.error(f"Verification failed: {e}")
