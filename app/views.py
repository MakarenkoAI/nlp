from django.shortcuts import render, redirect
from app.tools import *
from django.http import HttpResponse
__INPUT = None
__OUTPUT = None

def homePageView(request):
    global __INPUT
    global __OUTPUT
    if request.method == 'POST':
        print(";",request.POST)
        if request.POST.get("translate") != None and request.POST.get("input_text") != None:
            __INPUT = request.POST.get("input_text")
            __OUTPUT = algorithm2(__INPUT)
            saveSentences(__INPUT)
            return render(request, 'main_page.html', {'input': __INPUT, "output": __OUTPUT})  
        
        if request.POST.get("clear") != None:
            return render(request, 'main_page.html',  {'input': None, "output": None}) 
        
        if  request.POST.get("open") != None:
            file = request.FILES.get("file")
            if file:
                __INPUT = getPDFContent(file)
                return render(request, 'main_page.html', { 'input': __INPUT, "output": None }) 
            
        if request.POST.get("save") != None and request.POST.get("output_text") != None:
            __INPUT = request.POST.get("input_text")
            __OUTPUT = request.POST.get("output_text")
            writeInFile(__OUTPUT)
            return render(request, 'main_page.html', { 'input': __INPUT, "output": __OUTPUT}) 
        
        if request.POST.get("dictionary") != None:  
            return redirect('dictionary')
        
        if request.POST.get("savedict") != None:
            text = request.POST.get("dict_text")
            text = writeInFile(text)
            return render(request, 'dictionary.html', {'text': text})
        
        if request.POST.get("return") != None:
            return render(request, 'main_page.html',  { 'input': __INPUT, "output": __OUTPUT})
        
        if request.POST.get("searchdict") != None:
            substring = request.POST.get("searchdict")
            if substring == ',': return render(request, 'dictionary.html', {'text': None})
            lines = findLines(substring)
            return render(request, 'dictionary.html', {'text': lines})
        
        if request.POST.get("cleardict") != None:
            clearFile()
            return render(request, 'dictionary.html')
        
    return render(request, 'main_page.html')
    
def dictPageView(request):
    text = ''
    with open("dictionary.txt", 'r', encoding="utf-8") as file:
        text = file.read()
    return render(request, 'dictionary.html', {'text': text})

def saveSentences(text):
    with open("sentences.txt", "r", encoding="utf-8") as file:
        textOld= file.read()
        textOld = get_lines(textOld)
    with open("sentences.txt", "w", encoding="utf-8") as file:
        file.write(text)
        for el in textOld:
            if el not in text:
                file.write(el)

def getSentences():
    with open("sentences.txt", "r", encoding="utf-8") as file:
        return file.read()

def clear(word):
    word = word.replace("\r", "")
    word = word.replace("\t", "")
    word = word.replace("\n", "")
    return word

def parseTxtFile()-> dict:
    wordDictionary = {}
    with open("dictionary.txt", "r", encoding="utf-8") as file:
        text = file.read()
        sents = text.split('\n')
        sents = [clear(el) for el in sents]
        if len(sents) > 4:
            i = 0
            while i < len(sents)-4:
                wordDictionary.update({sents[i]:[sents[j] for j in range(i+1, i+5, 1)]})
                i +=5
    return wordDictionary

def get_text_from_dict(dictionary:dict)->str:
    text=""
    if len(dictionary) == 0 : return
    for key, value in dictionary.items():
        value1, value2, value3, value4 = value[0], value[1], value[2], value[3]
        text+=f"{key}\n\t{value1}\n\t{value2}\n\t{value3}\n\t{value4}\n"
    return text

def get_xml_text_from_dict(dictionary:dict)->str:
    text="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<text>\n"
    if len(dictionary) == 0 : return
    for key, value in dictionary.items():
        values = [v[v.find(":")+2:len(v)] for v in value]
        value1, value2, value3, value4 = values[0], values[1], values[2], values[3]
        text+=f"<w>{key} <ana lemma=\"{value1}\" text=\"{value2}\" pos=\"{value3}\" dep=\"{value4}\"/></w>\n"
    text += "</text>\n"
    return text

def writeInFile(output:str)->str :
    wordDictionary = parseTxtFile()
    sents = output.split('\n')
    sents = [clear(el) for el in sents]
    if len(sents) > 4:
        i = 0
        while i < len(sents)-4:
            wordDictionary.update({sents[i]:[sents[j] for j in range(i+1, i+5, 1)]})
            i +=5
    text = get_text_from_dict(wordDictionary)
    with open("dictionary.txt", "w", encoding="utf-8") as fileW:
        fileW.write(text)
    textXml = get_xml_text_from_dict(wordDictionary)
    with open("dictionary.xml", "w", encoding="utf-8") as fileW:
        fileW.write(textXml)
    return text

def clearFile():
    with open("dictionary.txt", "w", encoding="utf-8") as file:
       file.write("")

def findLines(substring:str)-> str:
    answer = []
    wordDictionary = parseTxtFile()
    with open("dictionary.txt", "r", encoding="utf-8") as file:
        text = file.read()
        text = text.split('\n')
        if substring == '.': return '\n'.join(text)
        for line in text:
            if substring == line:
                answer.append("<--------------Word-------------->\n")
                answer.append(line)
        __SENTENCES = getSentences()
        if substring in wordDictionary.keys() and __SENTENCES:
            answer.append('\n'.join(wordDictionary[substring]))
            answer.append("\n<--------------Concordance-------------->\n")
            lines = list(set(get_lines(__SENTENCES)))
            for line in lines:
                if substring in line:
                    answer.append(clear(line) + '\n')
    return '\n'.join(answer)
