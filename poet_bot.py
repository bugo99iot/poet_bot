import pandas as pd
import nltk
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
from nltk import word_tokenize
import time

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#upload dataframe
df = pd.read_csv("tokenized_poems.csv", header=None)
df=df.fillna(" ")
df.columns = ["text"]

def enter_string():
    time.sleep(1)
    print("Hello, this is Poet-Bot.")
    time.sleep(1)
    print("What kind of poem would you like to read?")
    time.sleep(1)
    search = input("Write something here: ")
    time.sleep(1)
    return search

def tokenize_string(string):
    ps = PorterStemmer()
    tokens = word_tokenize(string.lower())
    filtered_tokens = [ps.stem(word) for word in tokens if word not in stopwords.words('english') and bool(re.search("[-0123456789`>(</',;:!?.)]", word))==False]
    return filtered_tokens


def counts(row,filtered_tokens):
    tot=0
    for item in filtered_tokens:
        tot+=row.count(item)
    return tot

def main():
    search = enter_string()
    filtered_tokens = tokenize_string(search)
    df["counts"]=df["text"].apply(lambda row: counts(row, filtered_tokens))
    target_index = df["counts"].idxmax()
    target_count = df["counts"][target_index]
    return target_index, target_count

if __name__ == "__main__":
    target_index, target_count = main()

    if target_count == 0:
        while target_count == 0:
            print("Sorry, no match was found, try again!")
            target_index, target_count = main()

    df_poems = pd.read_csv("poems_collection.csv", header=None)
    df_poems.head()

    target_index = target_index + 1    

    print()
    print()
    print("Here is your poem: ")
    print()
    print()
    print(color.BOLD + df_poems.iloc[target_index,2].replace("<br/>","\n") + color.END)
    print()
    print()
    print(df_poems.iloc[target_index,1].replace("<br/>","\n").strip())
    print()
    print("by:", df_poems.iloc[target_index,0].replace("<br/>","\n"))
