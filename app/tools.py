import nltk
import nltk.corpus  
from nltk.text import Text  
from pypdf import PdfReader
from nltk.corpus import wordnet as wn
from nltk.draw import *
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import pprint
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer


nltk.download('gutenberg')
nltk.download('genesis')
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('state_union')

def percentage(word:str, text:Text): 
    return round(100*text.tokens.count(word)/len(text.tokens), 3)

def lexical_diversity(text:Text):
    return round(len(text.tokens)/len(set(text.tokens)), 3)

def percentage(word:str, text:list): 
    return round(100*text.count(word)/len(text), 3)

def lexical_diversity(text:list):
    return round(len(text)/len(set(text)), 3)

def getPDFContent(path:str):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def getLexName(word:str):
    answer = []
    for synset in wn.synsets(word):
        if synset.lexname() not in answer:
            answer.append(synset.lexname())
    return answer

def getDefinition(word:str):
    answer = []
    for synset in wn.synsets(word):
        if synset.definition() not in answer:
            answer.append(synset.definition())
    return list(set(answer))

def getExamples(word:str)-> list:
    answer = []
    for synset in wn.synsets(word):
        if synset.examples() not in answer:
            answer.append(synset.examples())
    return answer

def get_lines(text:str)-> list:
    return nltk.sent_tokenize(text)

def clean_text(text:list)-> list:
    clean_text = []
    for line in text:
        line = re.sub(r'x\d+', '', line)
        line = re.sub(r'\\n', '', line)
        line = re.sub(r'\s+', ' ', line)
        line = re.sub(r'- ', '', line)
        symbol = re.search(r"\d+", line)
        if line != '.' and symbol == None and ']' not in line and '[' not in line:
            clean_text.append(line)
    return clean_text

def get_split_lines(text:str)-> list:
    lines = clean_text(get_lines(text))
    return [nltk.word_tokenize(line) for line in lines]

def get_tokens(text:str)-> list:
    text = get_split_lines(text)
    return [nltk.pos_tag(line) for line in text]

__PATH = "Harry_Potter/HP1.pdf"

#moby = Text(nltk.corpus.gutenberg.words('melville-moby_dick.txt'))
#moby.concordance("Nick")

content = getPDFContent(__PATH)
split_lines = get_tokens(content)

grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}
        {<DT>?<JJ>*<NN>}  
        {<NNP>+}               
"""
cp = nltk.RegexpParser(grammar)
rezult = [cp.parse(line) for line in split_lines]
[line.draw() for line in rezult]

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

tokenized = custom_sent_tokenizer.tokenize(sample_text)
