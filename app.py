import streamlit as st
import pandas as pd
import requests
import io

# Optional: App title
st.title("📊 Anime Explorer with Jikan API")

# ✅ Usability goals section
st.markdown("""
## 🎯 Usability Goals

This anime discovery app aims to meet the following usability goals:

- **Effectiveness**: Allow users to quickly search for anime and retrieve detailed, accurate information.
- **Efficiency**: Display anime results and charts in under 1 second using fast, cached API responses.
- **Learnability**: Simple input boxes and checkboxes make the app intuitive for new users.
- **Memorability**: Clear layout and reusable filters help users remember how to perform tasks.
- **User Satisfaction**: Users enjoy browsing anime visually with images, charts, and feedback messages.
- **Error Prevention**: Input validation and feedback (e.g., “Anime not found”) guide users toward correct use.
""")




st.header("🔍 Search Anime by Title")

search_query = st.text_input("Enter an anime title (e.g., Naruto, Attack on Titan):")

if search_query:
    with st.spinner("Searching..."):
        search_url = f"https://api.jikan.moe/v4/anime?q={search_query}&limit=10"
        response = requests.get(search_url)

    if response.status_code == 200:
        results = response.json()["data"]


        if results:
            st.success(f"Found {len(results)} anime for '{search_query}'")

            # Create a DataFrame of results
            search_df = pd.DataFrame([{
                "Title": anime["title"],
                "Type": anime["type"],
                "Episodes": anime["episodes"],
                "Score": anime["score"],
                "Start Date": anime["aired"]["from"],
                "Rating": anime["rating"]
            } for anime in results])




            #Displays Table
            st.subheader("📋 Search Results Table")
            st.dataframe(search_df)

            # Conversion of DataFrame to CSV and encoding as bytes
            csv = search_df.to_csv(index=False)
            st.download_button(
                label="Downloaded Results in CSV Format",
                data=csv,
                file_name="anime_results.csv",
                mime="text/csv"
            )

            # Chart (if scores exist)
            st.subheader("📈 Score Comparison")
            score_df = search_df.dropna(subset=["Score"])
            if not score_df.empty:
                st.bar_chart(score_df.set_index("Title")["Score"])
            else:
                st.warning("No scores available to plot.")
        else:
            st.warning("No anime found.")
    else:
        st.error("Failed to retrieve data. Please try again later.")







        st.header("Anime Sudio with A Map of their Genre (Mock Data)")

        map_data = pd.DataFrame({
            'lat' : [35.6895, 34.6937,43.0667],
            'lon' : [139.6917, 135.5023,  141.3500],
            'label' : ['Studio Trigger(Tokoyo)', 'Kyoto Animation(Osaka', 'WIT Studio(Sapporo)']


        })

        # Shows the Map
        st.map(map_data)
        st.write("Mapped studios(mockcoordinates):")
        st.dataframe(map_data)





