import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

# Inisialisasi Session State untuk menyimpan data yang diunggah
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "data" not in st.session_state:
    st.session_state["data"] = None

with st.sidebar:
    menu = option_menu(
        menu_title = "Main Menu",
        options=["Business Case", "Upload File", "Weekly Analysis", "Sentiment Analysis", "Tier Analysis", "Top Media Outlet", "About Me"],
        icons=["house", "file-bar-graph", "filter-circle", "diagram-3","diagram-3", "database", "person"],
        menu_icon="cast",  # optional
        default_index=0,  # optional
        styles={

                "icon": {"color": "orange"},
                "nav-link": {
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )


# Upload File Tab
if menu == "Upload File":
    st.title("Upload Your Data File")
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    if uploaded_file:
        st.session_state["uploaded_file"] = uploaded_file
        df = pd.read_csv(uploaded_file)
        st.session_state["data"] = df
        st.success("File uploaded successfully!")
        st.write("Preview of your data:")
        st.dataframe(df.head())

# Gunakan data dari session state
if st.session_state["data"] is not None:
    df = st.session_state["data"]
    df['Date'] = pd.to_datetime(df['Date'])
    df['Week'] = df['Date'].dt.isocalendar().week

    # Aggregations
    weekly_data = df.groupby(['Week']).agg(
        total_coverage=('Media Outlet', 'count'),
        total_reach=('Estimated Reach', 'sum')
    ).reset_index()

    sentiment_data = df.groupby(['Sentiment']).agg(
        total_coverage=('Media Outlet', 'count'),
        total_reach=('Estimated Reach', 'sum')
    ).reset_index()

    tier_data = df.groupby(['Media Tier']).agg(
        total_coverage=('Media Outlet', 'count'),
        total_reach=('Estimated Reach', 'sum')
    ).reset_index()

    # Media outlet analysis
    df['Media Outlet'] = df['Media Outlet'].str.lower()
    outlet_data = df.groupby(['Media Outlet', 'Sentiment']).agg(
        total_coverage=('Media Outlet', 'count'),
        total_reach=('Estimated Reach', 'sum')
    ).reset_index()

    # Aggregate for all outlets
    outlet_totals = df.groupby('Media Outlet').agg(
        total_coverage=('Media Outlet', 'count'),
        total_reach=('Estimated Reach', 'sum')
    ).reset_index()

    # Calculate positive rate
    positive_counts = df[df['Sentiment'] == 'Positive'].groupby('Media Outlet').size().reset_index(name='positive_count')
    outlet_totals = outlet_totals.merge(positive_counts, on='Media Outlet', how='left').fillna(0)
    outlet_totals['positive_rate'] = (outlet_totals['positive_count'] / outlet_totals['total_coverage']) * 100

    # Sort by total coverage
    outlet_totals = outlet_totals.sort_values('total_coverage', ascending=False)

    # Business Case
    if menu == "Business Case":
        st.title("Business Case")
        st.write("""
            **Media Coverage Analysis Platform**
            
            Dalam era digital, analisis media memainkan peran penting untuk memahami efektivitas kampanye komunikasi 
            dan dampaknya terhadap audiens. Platform ini dirancang untuk membantu Anda dalam:
            
            1. **Mengukur Total Reach dan Coverage**: Menganalisis seberapa luas jangkauan pesan Anda di berbagai media.
            2. **Mengevaluasi Sentimen Media**: Memahami apakah sentimen liputan cenderung positif, negatif, atau netral.
            3. **Menganalisis Media Tier**: Mengetahui performa media berdasarkan tingkatannya.
            4. **Identifikasi Media Teratas**: Mengenali media mana yang memberikan kontribusi terbesar terhadap liputan dan jangkauan Anda.

            Dengan menggunakan data berbasis bukti, Anda dapat merancang strategi komunikasi yang lebih efektif dan 
            memastikan pesan Anda mencapai audiens yang tepat dengan dampak yang maksimal.
        """)

    # Weekly Analysis
    elif menu == "Weekly Analysis":
        st.title("Weekly Analysis")
        metric = st.selectbox("Select Metric", ["Total Coverage", "Total Reach"])
        y_axis = 'total_coverage' if metric == "Total Coverage" else 'total_reach'
        fig = px.line(weekly_data, x='Week', y=y_axis, title=f"{metric} Per Week")
        st.plotly_chart(fig)

    # Sentiment Analysis
    elif menu == "Sentiment Analysis":
        st.title("Sentiment Analysis")
        metric = st.selectbox("Select Metric", ["Total Coverage", "Total Reach"])
        y_axis = 'total_coverage' if metric == "Total Coverage" else 'total_reach'
        fig = px.pie(sentiment_data, names='Sentiment', values=y_axis, title=f"{metric} by Sentiment")
        st.plotly_chart(fig)

    # Tier Analysis
    elif menu == "Tier Analysis":
        st.title("Tier Analysis")
        metric = st.selectbox("Select Metric", ["Total Coverage", "Total Reach"])
        y_axis = 'total_coverage' if metric == "Total Coverage" else 'total_reach'
        fig = px.pie(tier_data, names='Media Tier', values=y_axis, title=f"{metric} by Media Tier")
        st.plotly_chart(fig)

    # Top Media Outlet
    elif menu == "Top Media Outlet":
        st.title("Top Media Outlet")
        st.write("### Media Outlet Rankings")
        st.write("Below is the table of all media outlets sorted by total coverage:")
        st.dataframe(outlet_totals[['Media Outlet', 'total_coverage', 'total_reach', 'positive_rate']])

    # About Me
    elif menu == "About Me":
        # Judul halaman
        st.header("About Me")

        st.write("- **Nama Lengkap:** Jayadi Butar Butar")
        st.write("- **Alamat:** Jakarta, Indonesia")
        st.write("- **Email:** jayadidetormentor@gmail.com")

        # Summary
        st.subheader("Summary")
        st.markdown(""" <div style="text-align: justify">    
        I'm a motivated Data Professional with a strong background in scientific research, Data Science, and Machine Learning. 
        Proficient in Python, Rstudio, SQL, and Spreadsheets, I excel in qualitative and quantitative research. 
        My dynamic academic journey honed my strategic thinking, leadership, and problem-solving skills.
        I derive valuable insights from complex datasets and excel in presenting them for data-driven decision-making. 
        Passionate about Statistics, Data Science, and AI, I aim to make a significant impact in the world of data.
        Eager to learn and grow, I stay updated with the latest industry advancements through active training and self-directed learning. 
        My goal is to leverage my skills in data analysis and machine learning to solve complex problems and achieve meaningful outcomes.
        If you're looking for a dedicated and analytical team player thriving in a data-driven environment, let's connect for outstanding results.
        """, unsafe_allow_html=True)


        # Tautan ke Akun Sosial Media
        st.subheader("Projects Portofolio")
        st.write("- [LinkedIn](https://www.linkedin.com/in/jayadib/)")
        st.write("- [rPubs](https://rpubs.com/JayadiB/)")
        st.write("- [GitHub](https://github.com/Jay4di)")
else:
    if menu != "Upload File":
        st.warning("Please upload a file in the 'Upload File' tab to continue.")
