import streamlit as st

st.title('Stock Market Random Seed Predictor')
ticker = st.text_input('Enter Stock Ticker Symbol', 'AAPL')

st.write(f'You entered: {ticker}')