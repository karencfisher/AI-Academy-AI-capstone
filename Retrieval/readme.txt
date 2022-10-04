Information Retrieval task

This is in aome ways an experiment, in that while using a vectorized approach to
storing and searching documents, I've also incorporated the option to filter
the documents also with FT-IDF. One also can limit the tokens to the top max_words. 
The hope is to make searches even more relevant.

How has it worked? Farily well. But it is experimental. ;)

Files:
retrieval.py: the CLI application to run
document_store.py: fetching and storing random Wikipedia documents
doc2GLOVE.py: all preprocessing of text for the KNN model
scikit_model: wraps the scikit-learn Nearest Neighbors model, as pipelin
              for both training and searching

To run from CLI:

>>python retrieval.py   

To use TF-IDF filetring:

>>python retrieval.py filter

With max_words, for example top 100:

>>python retrieval.py filter 100

THe model can also be experimented with using the test.ipynb notebook.
