import re
from sklearn.neighbors import NearestNeighbors

from doc2glove import Document2GLOVE

'''
The Model class essentially wraps the scikit-learn Nearest Neighbor
model. This implements a consistent pipeline for both training and
inference on a query.
'''
class Model:
    def __init__(self, n_nearest, glove_model):
        '''
        Constructor

        Inputs: n_nearest, int, number of matches to return
                glove_model, string, the Gensim GLOVE model to use
        '''
        self.vectorize_doc = Document2GLOVE(glove_model)
        self.KNN = NearestNeighbors(n_neighbors=n_nearest,
                                    metric='cosine',
                                    n_jobs=-1)

    def fit(self, documents, tfidf=False, max_words=None):
        '''
        Training the KNN model

        Inputs: documents, list, the untokenized documents
                tfidf, bool, whether to apply tfidf filtering (default is False)
                max_words, int, maximum tokens to apply to tf-idf
                scores if filtering chosen (default None)
        '''
        data = self.vectorize_doc.transform(documents, 
                                            tfidf=tfidf, 
                                            max_words=max_words)
        self.KNN.fit(data)
        return self.KNN

    def infer(self, query):
        '''
        Perform inference with a query

        Input: query, string, untokenized query
        Output: top n_neighbors matches
        '''
        # remove non-alpha numeric characters
        query = re.sub('[^\w\s]', '', query)
        
        data = self.vectorize_doc.transform([query])
        results = self.KNN.kneighbors(data)
        return results
