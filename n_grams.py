
from utils.data_utils import normalize_events,parse_log_file
from utils.markov_chain import generate_markov_chain, visualize_markov_chain
import os
import re
import pandas as pd
from collections import Counter
from itertools import islice
from mlxtend.frequent_patterns import apriori, association_rules

def generate_ngrams(sequence, n):
    return list(zip(*[islice(sequence, i, None) for i in range(n)]))

def analyze_common_sequences(file_path,parsetype=1, n_gram_size=2, min_support=0.5):

    # Iterate through each file
    data = pd.read_csv(file_path)
    embedding_input = pd.DataFrame(columns=["file", "parsed_events"])
    all_sequences = []
    for filename, events in data[['file','events']].values:

        # Parse the log events
        if parsetype==1:
          event_sequence = parse_log_file(events)
        else:
          event_sequence = normalize_events(events)


        all_sequences.append(event_sequence)


    # generate N-gram
    all_ngrams = [generate_ngrams(seq, n_gram_size) for seq in all_sequences]

    # calculate frequency
    flattened_ngrams = [item for sublist in all_ngrams for item in sublist]
    ngram_counts = Counter(flattened_ngrams)

    # filte low frequency gram out
    ngram_df = pd.DataFrame(ngram_counts.items(), columns=[f"{n_gram_size}-gram", "Count"])
    ngram_df = ngram_df.sort_values(by="Count", ascending=False)

    # transfer N-gram into Apriori needed（one-hot code）
    unique_ngrams = list(set(flattened_ngrams))

    transactions = []
    for ngram_list in all_ngrams:
        transaction = {ngram: (ngram in ngram_list) for ngram in unique_ngrams}
        transactions.append(transaction)

    df_transactions = pd.DataFrame(transactions)

    # run Apriori
    freq_items = apriori(df_transactions, min_support=min_support, use_colnames=True)

    print("🔍 popular sequence:")
    print(freq_items.sort_values(by="support", ascending=False))

    return ngram_df, freq_items
if __name__ == "__main__":
    file_path = '/Users/lijinxuan/Documents/abbthesis/master_thesis/data/select_premium0702.csv'
    # file_path = '/content/drive/MyDrive/data/select_premium0702.csv'
    
    ngram_df, freq_items = analyze_common_sequences(file_path,parsetype=1, n_gram_size=3, min_support=0.5)