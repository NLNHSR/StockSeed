import numpy as np

def similarity_score(stock_data, random_graphs):
    scores = []
    for random_graph in random_graphs:
        distance = np.linalg.norm(np.array(stock_data) - np.array(random_graph))
        score = -distance
        scores.append(score)
    
    return np.argmax(scores)

def generate_random_stock_data(num_days=252, seed=None, initial_price=100, mean=0, std_dev=0.01):
    if seed is not None:
        np.random.seed(seed)
    daily_returns = np.random.normal(mean, std_dev, num_days) 
    prices = initial_price * (1 + daily_returns).cumprod()
    return prices
    
def generate_multiple_random_graphs(num_graphs=1000, num_days=252, initial_price=100, mean=0, std_dev=0.01):
    random_graphs = []
    seeds = []
    for i in range(num_graphs):
        np.random.seed(None) 
        seed = np.random.randint(0, 4294967295)  
        prices = generate_random_stock_data(num_days, seed, initial_price, mean, std_dev)
        random_graphs.append(prices)
        seeds.append(seed)
    return random_graphs, seeds

def extend_random_stock_data(random_graph, num_extend=30, seed=None, mean=0, std=0.02):
    if seed is not None:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    
    last_price = random_graph[-1]
    daily_returns = rng.normal(mean, std, num_extend)
    extended_graph = last_price * (1 + daily_returns).cumprod()
    return np.concatenate([random_graph, extended_graph])
