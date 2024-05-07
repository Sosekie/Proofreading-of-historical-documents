# Proofreading-of-historical-documents

## Workflow

- Using [i2OCR](https://www.i2ocr.com/pdf-ocr-chinese-traditional) to get txt files.
- Translate traditional chinese character into simple one.
- Remove line breaks in txt to get two whole strings.
- Remove spaces and use any punctuation mark as a separator to get an array of strings.
- Use Bert to complete the embedding.
- Use Faiss to do the search.

## Environment

- conda create -n prhd python=3.9
- conda activate prhd
- pip install -r requirements.txt
- conda install -c pytorch faiss-gpu