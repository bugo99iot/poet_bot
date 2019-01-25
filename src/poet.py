from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
from nltk import word_tokenize

import nltk
nltk.download('punkt')
nltk.download('stopwords')


def tokenize_string(string):
    """

    :param string:
    :return:
    """
    ps = PorterStemmer()
    tokens = word_tokenize(string.lower())
    filtered_tokens = [ps.stem(word) for word in tokens if word not in stopwords.words('english') and bool(re.search("[-0123456789`>(</',;:!?.)]", word))==False]
    return filtered_tokens


def counts(row, filtered_tokens):
    """

    :param row:
    :param filtered_tokens:
    :return:
    """

    row_string = row.values[0]

    tot = 0
    for item in filtered_tokens:
        tot = row_string.count(item)
    return tot


def get_target_index(user_input_tokenized, df_tokenized):
    """

    :param user_input_tokenized:
    :param df_tokenized:
    :return:
    """

    df_tokenized["counts"] = df_tokenized.apply(lambda row: counts(row, user_input_tokenized), axis=1)
    target_index = df_tokenized["counts"].idxmax()
    target_count = df_tokenized["counts"][target_index]

    if target_count == 0:
        return None
    else:
        return target_index


class Poet(object):

    def __init__(self, user_input: str, df_tokenized, df_poems):
        """

        :param user_input:
        :param df_tokenized:
        :param df_poems:
        """
        self.user_input = user_input
        self.user_input_tokenized = tokenize_string(user_input) if self.user_input is not None else None

        self.df_tokenized = df_tokenized
        self.df_poems = df_poems

    @property
    def get_poem(self):

        if self.user_input_tokenized is None:
            return None

        target_index = get_target_index(user_input_tokenized=self.user_input_tokenized, df_tokenized=self.df_tokenized)

        if target_index is None:
            return None

        target_index = target_index

        title = self.df_poems.iloc[target_index,2].replace("<br/>", "\n")
        body = self.df_poems.iloc[target_index,1].replace("<br/>", "\n").strip()
        author = self.df_poems.iloc[target_index, 0].replace("<br/>", "\n")

        return {"title": title, "body": body, "author": author}
