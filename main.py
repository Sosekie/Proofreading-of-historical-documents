from util.dataset import load_and_process_text
from util.retrieval import bert_based
from util.save import save_to_csv

if __name__ == "__main__":

    # get sentences for each document
    filenames = ['dataset/art_and_science_simple_txt.txt', 'dataset/art_thesis_selection_txt.txt']
    documents = []
    for filename in filenames:
        document = load_and_process_text(filename)
        documents.append(document)

    queries, sentences = documents[0], documents[1]
    retrieval_pairs = bert_based(queries, sentences, k=3)

    # save_to_csv(retrieval_pairs, 'output.csv')
