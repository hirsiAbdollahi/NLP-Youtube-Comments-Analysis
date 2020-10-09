import nltk

import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from string import punctuation

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

wordnet_lemmatizer = WordNetLemmatizer()

class Preprocess:
    
    def __int__(self):
        pass


    def to_lower(self,text):
       
        return text.lower()

    def remove_numbers(self,text):
       
        output = ''.join(c for c in text if not c.isdigit())
        return output

    def remove_punct(self,text):
       
        return ''.join(c for c in text if c not in punctuation)

    def remove_tags(self,text):
       
        cleaned_text = re.sub('<[^<]+?>', '', text)
        return cleaned_text

    def word_tokenize(self,text):
       
        return [w for sent in nltk.sent_tokenize(text) for w in nltk.word_tokenize(sent)]

    def remove_stopwords(self,sentence):
        
        stop_words = stopwords.words('english')
        return ' '.join([w for w in nltk.word_tokenize(sentence) if not w in stop_words])


    def lemmatize(self,text):
        lemmatized_word = [wordnet_lemmatizer.lemmatize(word)for sent in nltk.sent_tokenize(text)for word in nltk.word_tokenize(sent)]
        return " ".join(lemmatized_word)


    def preprocess(self,text):
            
        lower_text = self.to_lower(text)
        lemmatized_sent = self.lemmatize(lower_text)
        clean_text = self.remove_numbers(lemmatized_sent)
        
        clean_text = self.remove_punct(clean_text)
        clean_text = self.remove_tags(clean_text)
        clean_text = self.remove_stopwords(clean_text)
        
        word_tokens = self.word_tokenize(clean_text)
        
        word_list = []
        for i in word_tokens:
            word_list.append(i)
        return word_list