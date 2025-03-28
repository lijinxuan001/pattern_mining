import os
import re
import pandas as pd
from collections import Counter
from itertools import islice
from mlxtend.frequent_patterns import apriori, association_rules
from utils.data_utils import normalize_events
# from google.colab import drive

# load Google Drive
# drive.mount("/content/drive", force_remount=True)

# load deleted_features.txt as delete /d_features

# Sample logs (same as user provided)
log_lines = [
    "00:00:36.8147456|ControllerConnectionState|{D36779C8-DDC9-4295-A0D9-BC3B0A096645}|1",
    "00:00:37.1937165|AddedController|{D36779C8-DDC9-4295-A0D9-BC3B0A096645}|VC|7.12.0.0",
    "00:00:43.8096871|ActiveWindowChanged|DelayLoadedWindow|ControllerBrowser",
    "00:00:56.8694018|ExecutingCommand|TextEditorShow|Activated",
    "00:00:57.7101821|ActiveWindowChanged|GenericControllerFileItemTextEditorWindow|NoId",
    "00:00:58.1290534|ExecutedCommand|TextEditorShow",
    "00:01:02.0301210|ActiveWindowChanged|DelayLoadedWindow|ControllerBrowser",
]




import os
import re
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def generate_markov_chain(file_path):
    # Regex to extract the event type (second field)
    data = pd.read_csv(file_path)

    # Step 1: Extract event sequences from all log files
    all_event_sequences = []
    for events in data['events'].values:
        all_event_sequences.append(normalize_events(events))

    # Step 2: Count event transitions
    transition_counts = defaultdict(lambda: defaultdict(int))
    for seq in all_event_sequences:
        for a, b in zip(seq, seq[1:]):
            transition_counts[a][b] += 1

    # Step 3: Compute transition probabilities
    transition_probs = {
        from_event: {
            to_event: count / sum(targets.values())
            for to_event, count in targets.items()
        }
        for from_event, targets in transition_counts.items()
    }

    return transition_probs

def visualize_markov_chain(transition_probs):
    # Step 4: Build a weighted directed graph with edge thickness and color for frequency
    G = nx.DiGraph()
    for from_event, targets in transition_probs.items():
        for to_event, prob in targets.items():
            G.add_edge(from_event, to_event, weight=prob)

    # Step 5: Define edge colors and widths based on weights
    edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
    max_weight = max(weights)
    edge_colors = ['red' if w > 0.6 else 'orange' if w > 0.3 else 'gray' for w in weights]
    edge_widths = [3 + 7 * (w / max_weight) for w in weights]

    # Step 6: Draw the full graph
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=edge_widths, edge_color=edge_colors, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}, font_size=9)

    plt.title("Markov Chain of Events with Edge Weight Highlighting", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()



