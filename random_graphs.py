import numpy as np

def generate_random_graphs(num_graphs, length):
    random_graphs = []
    seeds = []
    for _ in range(num_graphs):
        seed = np.random.randint(0, 4294967295)
        np.random.seed(seed)
        random_graph = np.cumsum(np.random.randn(length))  
        random_graphs.append(random_graph)
        seeds.append(seed)
    return random_graphs, seeds

def similarity_score(stock_data, random_graphs):
    scores = []
    for random_graph in random_graphs:
        score = np.corrcoef(stock_data, random_graph)[0, 1] # can change to dynamic time warping algorithm later
        scores.append(score)
    
    return np.argmax(scores)

def generate_random_stock_data(num_days=252, seed=None, initial_price=100, mean=0, std_dev=0.01):
    if seed is not None:
        np.random.seed(seed)
    daily_returns = np.random.normal(mean, std_dev, num_days) 
    prices = initial_price * (1 + daily_returns).cumprod()
    return prices
    
def generate_multiple_random_graphs(num_graphs=10, num_days=252, initial_price=100, mean=0, std_dev=0.01):
    random_graphs = []
    seeds = []
    for i in range(num_graphs):
        seed = np.random.randint(0, 4294967295)  
        prices = generate_random_stock_data(num_days, seed, initial_price, mean, std_dev)
        random_graphs.append(prices)
        seeds.append(seed)
    return random_graphs, seeds

