import nltk
import nltk.corpus  
from nltk.text import Text  
from pypdf import PdfReader
from nltk.corpus import wordnet as wn
from nltk.draw import *
import re
import spacy #another open-source library for NLP
from spacy import displacy

nlp = spacy.load('en_core_web_sm')
nltk.download('universal_tagset')
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')

def percentage(word:str, text:Text): 
    return round(100*text.tokens.count(word)/len(text.tokens), 3)

def lexical_diversity(text:Text):
    return round(len(text.tokens)/len(set(text.tokens)), 3)

def percentage(word:str, text:list): 
    return round(100*text.count(word)/len(text), 3)

def lexical_diversity(text:list):
    return round(len(text)/len(set(text)), 3)

def getPDFContent(path:str)-> str:
    print(path)
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
        #symbol = re.search(r"\d+", line)
        #symbol == None
        if line != '.' and ']' not in line and '[' not in line:
            clean_text.append(line)
    return clean_text

def get_split_lines(text:str)-> list:
    lines = clean_text(get_lines(text))
    return [nltk.word_tokenize(line) for line in lines]

def get_tokens(text:str)-> list:
    text = get_split_lines(text)
    return [nltk.pos_tag(line, tagset='universal') for line in text]

def get_grammar(lines:list)->list:
    global cp
    return [cp.parse(line) for line in lines]

def get_dictionary(rezult:list)->dict:
    dictionary = {}
    if len(rezult) == 0: return
    for sentence in rezult:
        for lexem in sentence:
            if lexem[0] not in __SIGNS:
                dictionary.update({lexem[0].lower() : lexem[1]})   
    return {key:dictionary[key] for key in sorted(dictionary)}

def get_text(dictionary:dict)->str:
    text=""
    if len(dictionary) == 0 : return
    for key, value in dictionary.items():
        text+=f"{key} : {value}\n"
    return text

def get_text2(dictionary:dict)->str:
    text=""
    if len(dictionary) == 0 : return
    for key, value in dictionary.items():
        value1, value2, value3 = value[0], value[1], value[2]
        text+=f"{key:<12} : {value1:<12}{value2:<20}{value3:<12}\n"
    return text

def algorithm2(text:str):
    lines = clean_text(get_lines(text))
    text_dict = get_tags(lines)
    return get_text2(text_dict)

__SIGNS = [',', '.', '&', '?', '!', '/', ':', '@', '\'', '`', '’', '-', '—', "”", "“", 's', '(', ')', ';']

def algorithm(text:str):
    lines = get_tokens(text)
    dict = get_dictionary(lines)
    return get_text(dict)

translation_dict = {"nsubj":"subject",
    "root":"predicative",
    "ROOT":"predicative",
    "dobj": "object",
    "amod":"attribute"}

def get_tags(sentences:str)->dict:
    text_dict = {}
    for line in sentences:
        doc = nlp(line)
        for token in doc:
            token_text = token.text
            token_pos = token.pos_
            token_dep = token.dep_
            if translation_dict.get(token.dep_) != None: token_dep = translation_dict[token.dep_]
            token_head = token.head.text
            text_dict.update({token_text : [token_pos, token_dep, token_head]})
    return {key:text_dict[key] for key in sorted(text_dict)}
  