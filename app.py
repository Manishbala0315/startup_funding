import streamlit as st
import pandas as  pd
import matplotlib.pyplot as plt

st.set_page_config(layout = 'wide', page_title = "Startup analysis")

df = pd.read_csv("startup_clean.csv")

def load_investor_details(investor):
    st.title(investor)
    ##load the recent five invesment if  the investore
    last5_df = df[df['investors'].str.contains('investor', na=False)].head(5)[
        ['date', 'startup', 'vertical', 'City  Location', 'round', 'amount']]
    st.subheader('Most Recent invesments')
    st.dataframe(last5_df)
## biggest invesment
    col1,col2 = st.columns(2)
    with col1:
        big_series = df[df['investors'].str.contains('investor', na=False)].groupby('startup')[
            'amount'].sum().sort_values(ascending=False).head(5)
        st.subheader('Biggest  invesments')
        fig, ax = plt.subplots()
        colors = ['red', 'blue', 'green', 'orange']

        ax.bar(big_series.index, big_series.values,color=colors)

        st.pyplot(fig)


st.sidebar.title("Startup funding analysis, By Manish bala")
option = st.sidebar.selectbox('selest One',['Overall Analysis','startup','Investor'])

if option =='Overall Analysis':
    st.title('overall Analysis')
elif option == 'startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup details')
    st.title("Startup Analysis")
else:
    selected_investore = st.sidebar.selectbox('Select Startup',set(investor.strip() for sublist in df['investors'].dropna().str.split(',') for investor in sublist))
    btn2 = st.sidebar.button('Find Investore Details')
    if btn2:
        load_investor_details(selected_investore)


