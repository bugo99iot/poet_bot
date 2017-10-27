import pandas as pd
import nltk
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
from nltk import word_tokenize
import time

#design a class that allows to enter a string and returns closest poem as list = [author, title, text]

#upload dataframe
df = pd.read_csv("tokenized_poems.csv", header=None)
df=df.fillna(" ")
df.columns = ["text"]

class Poet:
    def __init__(self,text_input):
        self.text_input=text_input

    def tokenize_string(self, string):  
        string = string
        ps = PorterStemmer()
        tokens = word_tokenize(string.lower())
        filtered_tokens = [ps.stem(word) for word in tokens if word not in stopwords.words('english') and bool(re.search("[-01234}{56789`>(</',;:!?.)]", word))==False]
        return filtered_tokens

    def counts(self,row,filtered_tokens):
        tot=0
        for item in filtered_tokens:
            tot+=row.count(item)
        return tot

    def get_index(self):
        search = str(self.text_input)
        print(search)
        filtered_tokens = self.tokenize_string(search)
        df["counts"]=df["text"].apply(lambda row: self.counts(row, filtered_tokens))
        target_index = df["counts"].idxmax()
        target_count = df["counts"][target_index]
        return target_index, target_count


    def get_poem(self):
        target_index, target_count = self.get_index()

        if target_count == 0:
            print("No match was found for the query: " + str(self.text_input))
            return ["Try with another query, such as: /poem summer day.","Sorry, no match was found","Nobody"]
        else:
            df_poems = pd.read_csv("poems_collection.csv", header=None)
            df_poems.head()
            target_index = target_index + 1    
            return [df_poems.iloc[target_index,1],df_poems.iloc[target_index,2],df_poems.iloc[target_index,0]]
 
