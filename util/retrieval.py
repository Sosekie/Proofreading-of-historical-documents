import faiss
import torch
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from util.metrics import extract_changes, calculate_jaccard_index

import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def bert_based(queries, sentences, k):
    model = SentenceTransformer(
        "bert-base-nli-mean-tokens",
        cache_folder="./.cache",
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    )
    sentence_embeddings = model.encode(sentences, show_progress_bar=True)

    d = sentence_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(sentence_embeddings)

    retrieval_pairs = []
    for idx, query in enumerate(tqdm(queries, desc="Retrieving pairs")):
        xq = model.encode([query])
        D, I = index.search(xq, k)

        if len(I) > 0:
            jaccard_index = calculate_jaccard_index(set(query), set(sentences[I[0][0]]))
            retrieval_pairs.append(
                {
                    "query": idx,
                    "most_similar_sentence": int(I[0][0]),
                    "query_content": query,
                    "sentence_content": sentences[I[0][0]],
                    "jaccard_index": jaccard_index,
                }
            )
            print(retrieval_pairs[-1])
        print('------------------------------------')

    return retrieval_pairs
