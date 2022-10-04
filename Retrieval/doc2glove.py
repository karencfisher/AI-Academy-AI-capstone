import numpy as np
from sklearn.preprocessing import RobustScaler

import nltk
from nltk.corpus import stopwords
import gensim
import gensim.downloader
from gensim.models import TfidfModel
from gensim.corpora import Dictionary

'''
Document2GLOVE class

This class encapsulates the whole process of taking the documents (text
filtered only of punctuation, line-breaks, and footnotes), and build
an array of document embeddings. This allows building a consistent pipeline
for both training the model on the documents, and making inference 
with a query.

It includes the option to filter documents for relevance or uniqueness
of tokens in each document, relative to the corpus as a whole. There is
also an option to discard tokens with tf-idf scores below a specificed 
threshold.

The basic path taken, depending on if the option to tf-if filter:

documents --> tokenize --> vectorize --> document vectors
                       |
                       |--> tf_idf filter --> vectorize --> document vectors
'''
class Document2GLOVE:
    def __init__(self, glove_model):
        '''
        Constructor

        Input: glove_model, the specific Gensim GLOVE model as a
               string
        '''
        self.GloveModel = gensim.downloader.load(glove_model)

    def __tokenize_doc(self, document):
        '''
        Tokenize a single document, filtering out also stopwords

        Input: document, the untokenized text
        Output: list of tokens
        '''
        tokens = nltk.tokenize.word_tokenize(document)
        tags = nltk.pos_tag(tokens)
        filtered_tokens = set()
        for tag in tags:
            if tag[0] in stopwords.words('english'):
                continue
            if tag[1] not in ['JJ', 'JJR', 'JJS']:
                filtered_tokens.add(tag[0])
        return filtered_tokens

    def __tf_idf(self, documents, max_words=None):
        '''
        TF-IDF filtering

        Input: documents, tokenized documents (list of lists of tokens)
               max_words, int maximum number of most relevant tokens (optional)
        Output: filtered documents (common terms discarded)
        '''
        dct = Dictionary(documents)
        corpus = [dct.doc2bow(line) for line in documents]
        model = TfidfModel(corpus)

        filtered_docs = []
        for index in range(len(corpus)):
            vector = (model[corpus[index]])
            if max_words is not None:
                vector.sort(key=lambda x: x[1])
                vector = vector[:max_words]
            filtered_doc = [dct[vect[0]] for vect in vector]
            filtered_docs.append(filtered_doc)
        return filtered_docs

    def __vectorize_doc(self, filtered_tokens):
        '''
        Vectorize a single document, as tokens

        Input: filetered_tokens, a tokenized and filtered document
        Output: document vector
        '''
        doc_vector = np.zeros(50)
        for Token in list(filtered_tokens):
            try:
                WordVectors = self.GloveModel[Token.lower()]
                doc_vector += np.array(WordVectors)
            except KeyError:
                continue

        # scale the vector
        scaler = RobustScaler()
        doc_vector = doc_vector.reshape(-1, 1)
        doc_vector = scaler.fit_transform(doc_vector)
        doc_vector = doc_vector.squeeze()

        return doc_vector

    def transform(self, documents, tfidf=False, max_words=None):
        '''
        Process the documents

        Input: documents, list of untokenized documents
               tfidf, bool, whether to apply tf-idf filtering (default is False)
               max_words, int, max number of tokens for tf-idf scores. Only applicable
                          if tfidf == True.
        Output: document vectors
        '''
        doc_tokens = [self.__tokenize_doc(doc) for doc in documents]
        if tfidf:
            doc_tokens = self.__tf_idf(doc_tokens, max_words=max_words)
        doc_vects = [self.__vectorize_doc(tokens) for tokens in doc_tokens]
        return doc_vects

    