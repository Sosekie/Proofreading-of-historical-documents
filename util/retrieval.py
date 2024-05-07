import faiss
import torch
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from utils.metrics import extract_changes, calculate_jaccard_index

import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def bert_based(diffs, k, logger):
    model = SentenceTransformer(
        "bert-base-nli-mean-tokens",
        cache_folder="./.cache",
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    )
    sentence_embeddings = model.encode(diffs, show_progress_bar=True)

    d = sentence_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(sentence_embeddings)

    retrieval_pairs = []
    for idx, diff in enumerate(tqdm(diffs, desc="Retrieving pairs")):
        xq = model.encode([diff])
        D, I = index.search(xq, k + 1)
        I = I[I != idx]
        logger.debug(f"Query: {idx} - Result: {I}")

        if len(I) > 0:
            # Extracts the changed rows from the diff string, filtering out the original data rows.
            query_set = extract_changes(diff)
            most_similar_set = extract_changes(diffs[I[0]])
            jaccard_index = calculate_jaccard_index(query_set, most_similar_set)
            logger.debug(
                f"Jaccard Index between Query {idx} and most similar diff {I[0]}: {jaccard_index}"
            )
            retrieval_pairs.append(
                {
                    "query": idx,
                    "most_similar_diff": int(I[0]),
                    "jaccard_index": jaccard_index,
                }
            )

    return retrieval_pairs
