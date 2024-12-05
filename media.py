import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load data
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Week'] = data['Date'].dt.to_period('W').astype(str)

    # Total reach and coverage per week, sentiment, and tier
    weekly_data = data.groupby('Week').agg({'Estimated Reach': 'sum', 'Article Link': 'count'}).reset_index()
    sentiment_data = data.groupby('Sentiment').agg({'Estimated Reach': 'sum', 'Article Link': 'count'}).reset_index()
    tier_data = data.groupby('Media Tier').agg({'Estimated Reach': 'sum', 'Article Link': 'count'}).reset_index()

    # Media outlet analysis
    media_outlet_data = data.groupby('Media Outlet').agg(
        {'Estimated Reach': 'sum', 'Article Link': 'count'}).reset_index()
    media_outlet_data['Sentiment Distribution'] = data.groupby('Media Outlet')['Sentiment'].apply(
        lambda x: x.value_counts(normalize=True).to_dict()
    )
    top_media_outlet = media_outlet_data.sort_values(by='Article Link', ascending=False).head(10)

    # Sidebar menu
    menu = st.sidebar.radio("Menu", ["Business Case", "Weekly Analysis", "Sentiment Analysis", 
                                     "Tier Analysis", "Top Media Outlet", "About Me"])

    if menu == "Weekly Analysis":
        st.title("Weekly Analysis")
        metric = st.selectbox("Choose Metric", ["Total Coverage", "Total Reach"])
        if metric == "Total Coverage":
            st.line_chart(weekly_data.set_index('Week')['Article Link'])
        else:
            st.line_chart(weekly_data.set_index('Week')['Estimated Reach'])

    elif menu == "Sentiment Analysis":
        st.title("Sentiment Analysis")
        metric = st.selectbox("Choose Metric", ["Total Coverage", "Total Reach"])
        if metric == "Total Coverage":
            st.pie_chart(sentiment_data.set_index('Sentiment')['Article Link'])
        else:
            st.pie_chart(sentiment_data.set_index('Sentiment')['Estimated Reach'])

    elif menu == "Tier Analysis":
        st.title("Tier Analysis")
        metric = st.selectbox("Choose Metric", ["Total Coverage", "Total Reach"])
        if metric == "Total Coverage":
            st.pie_chart(tier_data.set_index('Media Tier')['Article Link'])
        else:
            st.pie_chart(tier_data.set_index('Media Tier')['Estimated Reach'])

    elif menu == "Top Media Outlet":
        st.title("Top Media Outlet")
        st.write("Table of Top Media Outlets")
        st.table(top_media_outlet)

    elif menu == "About Me":
        st.title("About Me")
        st.write("This dashboard was created by [Your Name].")
