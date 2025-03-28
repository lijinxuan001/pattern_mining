from utils.data_utils import normalize_events
from utils.markov_chain import generate_markov_chain, build_graph_from_markov_chain
import os
import re
import pandas as pd
from collections import Counter
from itertools import islice
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pyvis.network import Network
import networkx as nx
from IPython.core.display import display, HTML
import webbrowser




if __name__ == "__main__":
    file_path = '/Users/lijinxuan/Documents/abbthesis/master_thesis/data/select_premium0702.csv'
    # file_path = '/content/drive/MyDrive/data/select_premium0702.csv'
    transition_probs = generate_markov_chain(file_path)
    G = build_graph_from_markov_chain(file_path)

    # 构建子图（例如只包含以 Command 开头的事件）
    prefix = "Command"
    nodes_to_include = [n for n in G.nodes if n.startswith(prefix)]
    subG = G.subgraph(nodes_to_include).copy()

    from pyvis.network import Network

    # Create pyvis network graph
    net = Network(height="750px", width="100%", directed=True, notebook=False, cdn_resources="in_line")

    # Add nodes and edges (show node names only on hover)
    for node in subG.nodes():
        net.add_node(node, label="", title=node)  # label="" hides it until hover

    for u, v, data in subG.edges(data=True):
        net.add_edge(u, v, value=data['weight'])

    # Save the interactive graph as HTML
    html_path = "command_subgraph.html"
    net.save_graph(html_path)

    print(f"✅ Graph saved: {html_path}")

    webbrowser.open(html_path)

    