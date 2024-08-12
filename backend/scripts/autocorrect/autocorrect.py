"""Module containing autocorrect functionalities."""
import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
import spacy
import contextualSpellCheck
import textdistance
from textblob import TextBlob

nltk.download('punkt')
# import contextualSpellCheck.data

class Autocorrect:
    """Master Autocorrect class to select and utiize a method."""
    def __init__(self) -> None:
        # self.models = [TextblobMethod(), SpacyContextualSpellCheckMethod()]
        self.model = TextblobMethod()

    def __call__(self, input_str: str):
        return self.model(input_str)

class EditDistanceMethod:
    """Autocorrect using Edit Distance method over the English Vocabulary."""
    def __init__(self) -> None:
        words = []
        with open('datasets/autocorrect/book.txt', 'r', encoding="utf-8") as f:
            file_name_data = f.read()
            file_name_data=file_name_data.lower()
            words = re.findall(r'\w+',file_name_data)

        self.v = set(words)

        self.word_freq = {}
        self.word_freq = Counter(words)

        self.probs = {}
        total = sum(self.word_freq.values())
        for k, v in self.word_freq.items():
            self.probs[k] = v/total

    def __call__(self, input_word: str):
        input_word = input_word.lower()
        if input_word in self.v:
            return input_word

        sim = [1-(textdistance.Jaccard(qval=2).distance(v,input_word)) for v in self.word_freq]
        df = pd.DataFrame.from_dict(self.probs, orient='index').reset_index()
        df = df.rename(columns={'index':'Word', 0:'Prob'})
        df['Similarity'] = sim
        output = df.sort_values(['Similarity', 'Prob'], ascending=False).head()
        return output

class SpacyContextualSpellCheckMethod:
    """Autocorrect by ContextualSpellCheck from Spacy"""
    def __init__(self) -> None:
        # df = pd.read_csv("datasets/train.csv")
        # first_column_list = df["text"].to_list()

        # vocab = Vocab(strings=first_column_list)
        self.nlp = spacy.load('en_core_web_sm') #, vocab=vocab)
        contextualSpellCheck.add_to_pipe(self.nlp)

    def __call__(self, input_str: str):

        # If input_str doesn't end with a period, add one
        if not input_str.endswith("."):
            input_str += "."

        doc = self.nlp(input_str)
        # return doc._.outcome_spellCheck

        if not doc._.performed_spellCheck:
            return []
        
        if not doc._.outcome_spellCheck:
            return []
        print("input string: \n", doc.text)
        print("outcome spell check: \n", doc._.outcome_spellCheck)
        print("score spell check: \n", doc._.score_spellCheck)
        if doc._.outcome_spellCheck in ("", "."):
            return []

        original_sentence_tokens = list(doc)
        sentences = []

        for token, suggestions in doc._.score_spellCheck.items():
            for suggestion in suggestions:
                temp = original_sentence_tokens.copy()
                text = suggestion[0]
                temp[token.i] = self.nlp(text)[0]
                sentences.append(" ".join([t.text for t in temp]).replace(" .", "."))

        return sentences

class TextblobMethod:
    """Autocorrect using textblob class."""
    def __init__(self):
        df = pd.read_csv("datasets/train.csv")
        text = " ".join(df["text"])
        tokens = word_tokenize(text.lower())
        self.vocab = set(tokens)

    def __call__(self, input_str: str):
        blob = TextBlob(input_str.lower())
        corrected_words = []
        for word in blob.words:
            suggestions = word.spellcheck()
            # Prioritize words from the vocabulary
            for suggestion, _ in suggestions:
                if suggestion in self.vocab:
                    corrected_words.append(suggestion)
                    break
            else:
            # If no suggestion from vocab, use TextBlob's first suggestion
                corrected_words.append(suggestions[0][0])
        corrected_str = " ".join(corrected_words)
        mod_inp = " ".join(blob.words)
        print(mod_inp, corrected_str)
        changed = corrected_str != mod_inp
        return corrected_str, changed

# input_str = "I lost my crd"
# # ac = SparkNLPMethod()
# ac = Autocorrect()
# print(ac(input_str))
