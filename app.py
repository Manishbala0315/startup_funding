import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai

# Set OpenAI API Key
openai.api_key = "import OpenAI from "openai";
const openai = new OpenAI();
const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    store: true,
    messages: [
        {"role": "user", "content": "write a haiku about ai"}
    ]
});
"  # Replace with your actual API key

st.set_page_config(layout='wide', page_title="Startup Analysis")

df = pd.read_csv("startup_clean.csv")

def load_investor_details(investor):
    st.title(investor)
    
    # Load the recent five investments of the investor
    last5_df = df[df['investors'].str.contains(investor, na=False)].head(5)[
        ['date', 'startup', 'vertical', 'City  Location', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)
    
    # Biggest investments
    col1, col2 = st.columns(2)
    with col1:
        big_series = df[df['investors'].str.contains(investor, na=False)].groupby('startup')[
            'amount'].sum().sort_values(ascending=False).head(5)
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        colors = ['red', 'blue', 'green', 'orange']
        ax.bar(big_series.index, big_series.values, color=colors)
        st.pyplot(fig)

def generate_insights():
    prompt = f"Analyze the startup investment trends in India based on the following data: {df.head(10).to_string()}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a data analysis assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

st.sidebar.title("Startup Funding Analysis, By Manish Bala")
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')
    
    if st.sidebar.button("Generate AI Investment Insights"):
        insights = generate_insights()
        st.subheader("AI-Generated Investment Insights")
        st.write(insights)

elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title("Startup Analysis")
else:
    selected_investor = st.sidebar.selectbox('Select Investor',
        set(investor.strip() for sublist in df['investors'].dropna().str.split(',') for investor in sublist))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)

st.sidebar.subheader("Ask AI about Startup Data")
user_question = st.sidebar.text_input("Type your question here...")

if st.sidebar.button("Ask AI"):
    prompt = f"Answer the question based on the given startup investment data: {df.to_string()}\n\nQuestion: {user_question}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    st.subheader("AI Response")
    st.write(response["choices"][0]["message"]["content"])
