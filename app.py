import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

st.set_page_config(layout='wide', page_title="Startup Analysis", page_icon="🚀")
st.markdown("""
    <style>
        .stApp { background-color: #f5f5f5; }
        .stTitle { color: #ff4b4b; text-align: center; font-size: 36px; font-weight: bold; }
        .stSidebar { background-color: #222; color: white; }
        .stDataFrame { border-radius: 15px; }
        .stPlot { border-radius: 15px; background-color: white; padding: 20px; }
        .stHeader { color: #ffd700; font-size: 28px; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Load the dataset
df = pd.read_csv("startup_clean.csv")
df.columns = df.columns.str.strip()


def load_investor_details(investor):
    st.markdown(f"<h1 class='stTitle'>{investor}</h1>", unsafe_allow_html=True)
    investor_df = df[df['investors'].str.contains(investor, na=False, case=False)]

    st.subheader('Most Recent Investments')
    st.dataframe(investor_df.head(5)[['date', 'startup', 'vertical', 'City  Location', 'round', 'amount']])

    st.subheader('Biggest Investments')
    big_series = investor_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=big_series.index, y=big_series.values, ax=ax, palette=['red', 'yellow', 'green'])
    ax.set_title("Top 5 Investments")
    ax.set_ylabel("Funding Amount")
    st.pyplot(fig)

    st.subheader("Investment Spiral Chart")
    theta = np.linspace(0, 4 * np.pi, len(big_series))
    r = big_series.values
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(theta, r, marker='o', color='magenta', linestyle='dashed')
    ax.set_title("Investment Spiral Chart")
    st.pyplot(fig)


def overall_analysis():
    st.markdown("<h1 class='stTitle'>Overall Startup Funding Analysis</h1>", unsafe_allow_html=True)

    st.subheader("Top 10 Funded Startups")
    top_startups = df.groupby('startup')["amount"].sum().sort_values(ascending=False).head(10)
    st.dataframe(top_startups)

    st.subheader("City-wise Investment Distribution")
    city_funding = df.groupby('City  Location')["amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    city_funding.head(10).plot(kind='bar', ax=ax, color='yellow')
    ax.set_title("Top 10 Cities by Investment")
    ax.set_ylabel("Total Funding")
    st.pyplot(fig)

    st.subheader("Sector-wise Funding")
    sector_funding = df.groupby('vertical')["amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=sector_funding.head(10).index, y=sector_funding.head(10).values, ax=ax,
                palette=['red', 'yellow', 'green'])
    ax.set_title("Top 10 Sectors by Investment")
    ax.set_ylabel("Total Funding")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Year-wise Funding Trend")
    df['year'] = pd.to_datetime(df['date']).dt.year
    yearly_funding = df.groupby('year')["amount"].sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=yearly_funding.index, y=yearly_funding.values, marker='o', ax=ax, color='green')
    ax.set_title("Yearly Funding Trend")
    ax.set_ylabel("Total Funding")
    st.pyplot(fig)

    st.subheader("Monthly Investment Trend")
    df['month'] = pd.to_datetime(df['date']).dt.to_period("M")
    monthly_funding = df.groupby('month')["amount"].sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=monthly_funding.index.astype(str), y=monthly_funding.values, marker='o', ax=ax, color='red')
    ax.set_title("Monthly Funding Trend")
    ax.set_ylabel("Total Funding")
    plt.xticks(rotation=45)
    st.pyplot(fig)


st.sidebar.markdown("<h1 style='color: white;'>Startup Funding Analysis, By Manish Bala</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    overall_analysis()

elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].dropna().unique().tolist()))
    if st.sidebar.button('Find Startup Details'):
        st.markdown(f"<h1 class='stTitle'>Analysis of {selected_startup}</h1>", unsafe_allow_html=True)
        startup_df = df[df['startup'] == selected_startup]
        st.dataframe(startup_df)

else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(
        set(investor.strip() for sublist in df['investors'].dropna().str.split(',') for investor in sublist)))
    if st.sidebar.button('Find Investor Details'):
        load_investor_details(selected_investor)
