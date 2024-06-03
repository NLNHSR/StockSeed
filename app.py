import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from fetch_data import fetch_stock_data
from random_graphs import generate_multiple_random_graphs, similarity_score, extend_random_stock_data

st.set_page_config(
    page_title="StockSeed",
    page_icon="🌱",
)

st.markdown("<h1 style='text-align: center; color: white;'>StockSeed</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #4CBB17; font-size: 18px'>Harnessing random graph seeds to overlay and \"predict\" stock market trends.</h2>", unsafe_allow_html=True)

ticker = st.text_input('Enter Stock Ticker Symbol', 'AAPL')
st.expander("Additional Parameters", expanded=False)
with st.expander("Additional Parameters"):
    std = st.slider('Standard Deviation:', min_value=0.0001, max_value=0.2, value=0.02, step=0.01)
    mean = st.slider('Mean:', min_value=0.0, max_value=0.5, value=0.0, step=0.01)
    num_graphs = st.slider('Number of Random Graphs:', min_value=100, max_value=10000, value=1000, step=100)
    num_extend = st.slider('Number of Days to Extend:', min_value=1, max_value=365, value=30, step=1)
    stock_period = st.selectbox('Stock history:', ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"),index=5)

col1, col2 = st.columns([1,1]) 
generate = False
extend = False

with col1:
    generate = st.button("Generate Best Random Graph", use_container_width=True)

with col2:
    extend = st.button("Extend Graph", use_container_width=True)


def plot_graph(random_graph, stock_data):
    df = pd.DataFrame({
        'Random Graph': random_graph,
        'Stock Data': stock_data
    })

    df['Day'] = df.index
    df = df.melt('Day', var_name='Category', value_name='Price')

    color_scale = alt.Scale(domain=['Random Graph', 'Stock Data'], range=['#4CBB17', '#FFFFFF'])

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('Day', title='# Days From Start Of Stock Period'),
        y=alt.Y('Price', title='Closing Price ($)', scale=alt.Scale(zero=False)),
        color=alt.Color('Category', scale=color_scale, legend=alt.Legend(title="Legend")),
    ).properties(width=700, height=400).configure_axis(
        gridColor='#8A9A5B4D',
        labelFontSize=12,
        titleFontSize=14,
        labelColor='white',
        titleColor='white'
    ).configure_legend(
        titleColor='white',
        labelColor='white'
    )

    st.altair_chart(chart)


if generate:
    stock_data = fetch_stock_data(ticker, stock_period)
    
    graphs, seeds = generate_multiple_random_graphs(num_graphs=num_graphs, num_days=len(stock_data), initial_price=stock_data[0], mean=mean, std_dev=std)
    best_index = similarity_score(stock_data, graphs)
    
    st.write(f"Best seed: {seeds[best_index]}")
    
    plot_graph(graphs[best_index], stock_data)
    
    st.session_state['stock_data'] = stock_data
    st.session_state['best_seed'] = seeds[best_index]
    st.session_state['best_graph'] = graphs[best_index]
    
if extend:
    if 'stock_data' in st.session_state and 'best_seed' in st.session_state and 'best_graph' in st.session_state:
        stock_data = st.session_state['stock_data']
        best_seed = st.session_state['best_seed']
        best_graph = st.session_state['best_graph']
        
        best_graph = extend_random_stock_data(best_graph, num_extend=num_extend, seed=best_seed, std=std)
        stock_data = np.concatenate([stock_data, [np.nan]*num_extend])
        
        st.write(f"Extending graph with seed: {best_seed}")
        
        plot_graph(best_graph, stock_data)
        
    else:
        st.write("Please generate the best random graph first.")

        
st.write("#")
st.write("#")
with st.expander("How it works"):
    st.write("""
            StockSeed generates multiple random stock price graphs and compares them to historical stock data to find the closest match using Euclidean distance. 
            Enter a stock ticker and adjust parameters like volatility, mean return, number of graphs, extension days, and data period. 
            StockSeed fetches historical prices, generates random graphs using a random walk process with specified mean and volatility, 
            and identifies the graph that most closely matches the historical data. The matching graph is displayed overlaid with the historical data, 
            and you can extend it further using the same random seed. This tool provides an interactive way to visualize and extend randomly generated stock trends.
            """)