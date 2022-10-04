import json
import requests
import re
from urllib.parse import quote as url_encode
import numpy as np
from bs4 import BeautifulSoup

from doc2glove import Document2GLOVE

'''
DocumentStore class is where we acquire and store randomly chosen
Wikipedia documents.

Each document is filtered of punctuation, special characters, footnotes
(numbers within square brackets such as '[12]'), and then stored. Also
the titles and URLs are recorded in a dictionary, with the keys the indexes
of the individual texts in the "tank" of documents.
'''
class DocumentStore:
    def __init__(self):
        self.base_url = 'https://en.wikipedia.org/'
        self.count = 0

        # dictionary of titles and URLS, by index
        self.documents = {}

        # 'tank' of documents
        self.texts = []
        
    def __get_titles(self):
        '''
        Get random wikipedia article titles using Wikipedia
        API.

        Output: list of titles
        '''
        titles = []
        
        # query the Wikipedia API for random articles
        query = 'w/api.php?action=query&list=random&format=json&rnnamespace=0'
        url = self.base_url + query + f'&rnlimit={self.count}'
        req = requests.get(url)

        # translate into json object and extract titles
        info = json.loads(req.text)
        for item in info['query']['random']:
            titles.append(item['title'])
        return titles

    def __get_document(self, title):
        '''
        Fetch a document from Wikipedia by title, and do basic
        filtering of the text

        Input: title, string, title of article
        Output: text and the URL to the page
        '''
        # URL encode the title and request page
        url = self.base_url + f'wiki/{url_encode(title)}'
        page = requests.get(url)

        # load HTML page into BeautifulSoup and extract all content
        # in <p> tags. This seems to give us the bulk of the contents.
        soup = BeautifulSoup(page.text, 'html.parser')
        paragraphs = soup.find_all('p')

        # filter each paragraph
        paras = []
        for paragraph in paragraphs:
            text = paragraph.text.lower()
            text = re.sub('\[\d+\]', '', text)
            text = re.sub('\n', ' ', text)
            text = re.sub('[^\w\s]', '', text)
            paras.append(text.strip())

        # render paragraphs into one document
        text = ' '.join(paras)
        return text, url   

    def load_documents(self, count):
        '''
        Load documents, get count random pages and process/store

        Input: count, int, number of documents to fetch
        '''
        self.count = count
        titles = self.__get_titles()

        for index, title in enumerate(titles):
            text, url = self.__get_document(title)
            self.documents[index] = {'title': title, 'url': url}
            self.texts.append(text)
