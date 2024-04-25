import nltk
from nltk.draw import *
import spacy
from spacy import displacy

nlp=spacy.load('en_core_web_sm')


nltk.download('averaged_perceptron_tagger')

from nltk import pos_tag, RegexpParser
from nltk.tokenize import word_tokenize

from nltk.corpus import wordnet 


def getMeaning(word:str)->str:
    syns = wordnet.synsets(word) 
    meaning = ''
    for el in syns:
        meaning += el.lemmas()[0].name() + ' <=> ' + el.definition() + '\n'
    return meaning

sentence = "The cat is sitting on the mat."

def getTree(sent:str)->None:
    tokens = word_tokenize(sentence)
    pos_tags = pos_tag(tokens)
    grammar = r""" 
    NP: {<DT>?<JJ>*<NN>}
    NP  VP: {<VB.*><NP|PP>?}
    VP  PP: {<IN><NP>} # PP  """ 
    parser = RegexpParser(grammar)
    parse_tree = parser.parse(pos_tags)
    parse_tree.pretty_print()

def getSemanticInfo(doc):
    info = []
    for token in doc:
        info.append(token.text)
    return '\n'.join(info)

def getImage(text:list):
    # Creating Doc object
    i = 0
    image = []
    info = ''
    links = []
    for sentence in text:
        doc=nlp(sentence)
        for token in doc:
            info += token.text + ' => ' + token.dep_ + '\n'
        image.append(displacy.render(doc, style='dep')) 
        with open("app/static/images/data" + str(i) + ".svg", "w") as file:
            if image[-1] != None:
                file.write(image[-1])
        links.append("static\images\data"+str(i)+".svg")
        info+='\n\n'
        i+=1
    return info, links
