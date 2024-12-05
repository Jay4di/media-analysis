import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import plotly.express as px

# Fungsi untuk membuat pie chart interaktif
def create_pie_chart_plotly(data, column_name):
    # Hitung jumlah untuk setiap kategori dalam kolom tertentu
    data_count = data[column_name].value_counts().reset_index()
    data_count.columns = [column_name, 'Count']
    
    # Plot pie chart interaktif
    fig = px.pie(data_count, names=column_name, values='Count', title=f"{column_name} Distribution")
    st.plotly_chart(fig)

# Load data
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Week'] = data['Date'].dt.to_period('W').astype(str)

    # Total reach and coverage per week, sentiment, and tier
    # Total reach per minggu
    total_reach_week = data.groupby('Week')['Estimated Reach'].sum().reset_index()
    total_reach_week.rename(columns={'Estimated Reach': 'Total Reach'}, inplace=True)

    # Total coverage (jumlah media outlet unik per minggu)
    total_coverage_week = data.groupby('Week')['Media Outlet'].count().reset_index()
    total_coverage_week.rename(columns={'Media Outlet': 'Total Coverage'}, inplace=True)

    # Gabungkan hasil
    weekly_data = pd.merge(total_reach_week, total_coverage_week, on='Week')
    sentiment_data = data.groupby('Sentiment').agg({'Estimated Reach': 'sum', 'Article Link': 'count'}).reset_index()
    tier_data = data.groupby('Media Tier').agg({'Estimated Reach': 'sum', 'Article Link': 'count'}).reset_index()


    # Media outlet analysis
    media_outlet_data = data.groupby('Media Outlet').agg(
        {'Estimated Reach': 'sum', 'Article Link': 'count'}).reset_index()

    # Tambahkan distribusi sentimen per media outlet
    sentiment_distribution = data.groupby('Media Outlet')['Sentiment'].apply(
        lambda x: x.value_counts(normalize=True).to_dict()
    ).reset_index(name='Sentiment Distribution')

    # Gabungkan data distribusi sentimen dengan media_outlet_data
    media_outlet_data = media_outlet_data.merge(sentiment_distribution, on='Media Outlet', how='left')

    top_media_outlet = media_outlet_data.sort_values(by='Article Link', ascending=False).head(10)

    # Sidebar menu
    menu = st.sidebar.radio("Menu", ["Business Case", "Weekly Analysis", "Sentiment Analysis", 
                                     "Tier Analysis", "Top Media Outlet", "About Me"])

    if menu == "Weekly Analysis":
        st.title("Weekly Analysis")
        metric = st.selectbox("Choose Metric", ["Total Coverage", "Total Reach"])
        if metric == "Total Coverage":
            st.line_chart(weekly_data.set_index('Week')['total_coverage_week'])
        else:
            st.line_chart(weekly_data.set_index('Week')['total_reach_week'])

    elif menu == "Sentiment Analysis":
        st.title("Sentiment Analysis")
        metric = st.selectbox("Choose Metric", ["Total Coverage", "Total Reach"])
        if metric == "Total Coverage":
            # Misalnya menggunakan plotly untuk Sentiment Analysis
            create_pie_chart_plotly(sentiment_data, 'Article Link')
        else:
            create_pie_chart_plotly(sentiment_data, 'Estimated Reach')

    elif menu == "Tier Analysis":
        st.title("Tier Analysis")
        metric = st.selectbox("Choose Metric", ["Total Coverage", "Total Reach"])
        if metric == "Total Coverage":
            create_pie_chart_plotly(tier_data, 'Article Link')
        else:
            create_pie_chart_plotly(tier_data, 'Estimated Reach')

    elif menu == "Top Media Outlet":
        st.title("Top Media Outlet")
        st.write("Table of Top Media Outlets")
        st.table(top_media_outlet)

    elif menu == "About Me":
        st.title("About Me")
        st.write("This dashboard was created by [Your Name].")
