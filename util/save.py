import pandas as pd

def save_to_csv(retrieval_pairs, filename):
    df = pd.DataFrame(retrieval_pairs)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f'Data saved to {filename}')