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

if generate:
    stock_data = fetch_stock_data(ticker, stock_period)
    
    graphs, seeds = generate_multiple_random_graphs(num_graphs=num_graphs, num_days=len(stock_data), initial_price=stock_data[0], mean=mean, std_dev=std)
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
        color=alt.value('#4CBB17')
    ).properties( width=800, height=400 )

    stock_data_line = base.encode(
        y=alt.Y('Stock Data', scale=alt.Scale(zero=False)),
        color=alt.value('white')
    ).properties( width=800, height=400 )

    chart = alt.layer(random_graph_line, stock_data_line).resolve_scale(
        y='shared'
    ).configure_axis(labelFontSize=12, titleFontSize=14)

    st.altair_chart(chart)
    
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
        df = pd.DataFrame({ 
            'Random Graph': best_graph,
            'Stock Data': stock_data
        })
        
        df['Day'] = df.index
        base = alt.Chart(df.reset_index()).mark_line().encode(x='Day')
        random_graph_line = base.encode(
            y=alt.Y('Random Graph', scale=alt.Scale(zero=False)),
            color=alt.value('#4CBB17')
        ).properties( width=800, height=400 )

        stock_data_line = base.encode(
            y=alt.Y('Stock Data', scale=alt.Scale(zero=False)),
            color=alt.value('white')
        ).properties( width=800, height=400 )

        chart = alt.layer(random_graph_line, stock_data_line).resolve_scale(
            y='shared'
        ).configure_axis(labelFontSize=12, titleFontSize=14)

        st.altair_chart(chart)
        
    else:
        st.write("Please generate the best random graph first.")