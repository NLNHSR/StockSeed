import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from fetch_data import fetch_stock_data
from random_graphs import generate_multiple_random_graphs, similarity_score

st.title('Stock Market Random Seed Predictor')
ticker = st.text_input('Enter Stock Ticker Symbol', 'AAPL')
std = st.slider('Choose Volatility', min_value=0.0001, max_value=0.2, value=0.02, step=0.01)

if st.button('Predict'):
    stock_data = fetch_stock_data(ticker)
    
    graphs, seeds = generate_multiple_random_graphs(num_graphs=100000, num_days=len(stock_data), initial_price=stock_data[0], mean=0, std_dev=std)
    best_index = similarity_score(stock_data, graphs)
    
    st.write(f"Best seed: {seeds[best_index]}")
    
    df = pd.DataFrame({
        'Random Graph': graphs[best_index],
        'Stock Data': stock_data
    })

    df['Day'] = df.index
    base = alt.Chart(df.reset_index()).mark_line().encode(x='Day')
    random_graph_line = base.encode(
        y=alt.Y('Random Graph', scale=alt.Scale(zero=False)),
        color=alt.value('green')
    ).properties( width=800, height=400 )

    stock_data_line = base.encode(
        y=alt.Y('Stock Data', scale=alt.Scale(zero=False)),
        color=alt.value('white')
    ).properties( width=800, height=400 )

    chart = alt.layer(random_graph_line, stock_data_line).resolve_scale(
        y='shared'
    ).configure_axis(labelFontSize=12, titleFontSize=14)

    st.altair_chart(chart)
    