import sys
import pandas as pd

from document_store import DocumentStore
from scikit_model import Model


# command line argument handling. 
max_words = None
tfidf = len(sys.argv) > 1 and sys.argv[1] == 'filter'
if tfidf:
    if len(sys.argv) > 2:
        max_words = int(sys.argv[2])
    print(f'TF-IDF filtering with maximum number of tokens = {max_words}')   

# Ask how many documents to fetch and fetch them
doc_store = DocumentStore()
correct = False
while not correct:
    n_documents = int(input('How many documents to fetch? (minimum 5) '))
    correct = n_documents >= 5
print(f'Fetching {n_documents} documents...')
doc_store.load_documents(n_documents)
print('Done!')

# List what we fetched, with titles and URLs
documents = doc_store.documents
listings = [[v['title'], v['url']] for v in documents.values()]
print('\ndocuments fetched:\n')
for listing in listings:
    print(f'{listing[0]}:\t\t {listing[1]}')

# build/train the model
print('\nBuilding the model, this may take a moment or two...')
model = Model(3, 'glove-twitter-50')
model.fit(doc_store.texts, tfidf=tfidf, max_words=max_words)
print('Done!\n')

# loop to perform searches on user queries
finish = False
while not finish:
    query = input('Enter a query, just <enter> to quit: ')
    if len(query) == 0:
        finish = True
        continue

    # extract results
    results = model.infer(query)
    matches = results[1][0]
    metrics = results[0][0]
    top_matches = []
    for i, m in enumerate(matches):
        document = doc_store.documents[m]
        match = [document['title'], document['url'], 1 - metrics[i]]
        top_matches.append(match)

    # make into a table and print
    table = pd.DataFrame(top_matches, columns=['Title', 'URL', 'Similarity'])
    print(f'\nQuery was "{query}".\nTop three matches:\n\n{table}\n')
