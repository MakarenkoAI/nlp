from django.shortcuts import render, redirect
from app.tools import *
from app.syntax_analysis import *
from django.http import HttpResponse
__INPUT = None
__OUTPUT = None

def homePageView(request):
    global __INPUT
    global __OUTPUT
    
    if request.POST.get("translate") and request.POST.get("input_text"):
        __INPUT = request.POST.get("input_text")
        lines = get_lines(__INPUT)
        __OUTPUT, content = getImage(lines)
        return render(request, 'main_page.html', {'input': __INPUT, "output": __OUTPUT, "image" : content})  
    
    if request.POST.get("clear"):
        return render(request, 'main_page.html',  {'input': None, "output": None}) 
    
    if  request.POST.get("open"):
        file = request.FILES.get("file")
        print(file)
        if file:
            __INPUT = clear(getPDFContent(file))
            return render(request, 'main_page.html', { 'input': __INPUT, "output": None }) 
        
    if request.POST.get("save") and request.POST.get("output_text"):
        __INPUT = request.POST.get("input_text")
        __OUTPUT = request.POST.get("output_text")
        writeInFile(__OUTPUT)
        return render(request, 'main_page.html', { 'input': __INPUT, "output": __OUTPUT}) 
    
    if request.POST.get("dictionary"):  
        return redirect('dictionary')
        
    return render(request, 'main_page.html')
    
def dictPageView(request):
    text = ''
    with open("dictionary.txt", 'r', encoding="utf-8") as file:
        text = file.read()
    if not len(request.POST): return render(request, 'dictionary.html', {'text': text})

    if request.POST.get("searchdict") != '':
        substring = request.POST.get("searchdict")
        lines = findLines(substring)
        return render(request, 'dictionary.html', {'text': lines})
    if request.POST.get("savedict"):
        text = request.POST.get("dict_text")
        writeInFile(text)
        return render(request, 'dictionary.html', {'text': text})
    if request.POST.get("return") == 'Return':
        return redirect('home')
    if request.POST.get("cleardict"):
        clearFile()
        return render(request, 'dictionary.html')

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

def clear(word:str):
    word = word.replace("\r", "")
    word = word.replace("\t", "")
    word = word.replace("\n\n", "")
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

def writeInFile(output:str) :
    rez = ''
    with open("dictionary.txt", "r", encoding="utf-8") as fileW:
        text = fileW.read()
        output = get_lines(output)
        for el in output:
            if el not in text:
                rez += '\n' + el
    with open("dictionary.txt", "w", encoding="utf-8") as file:
        file.write(clear(rez))
    return

def clearFile():
    with open("dictionary.txt", "w", encoding="utf-8") as file:
       file.write("")

def findLines(substring:str)-> str:
    if not substring: return ''
    answer = []
    with open("dictionary.txt", "r", encoding="utf-8") as file:
        text = file.read()
        text = text.split('\n')
        if substring == '.': return '\n'.join(text)
        for line in text:
            if substring in line:
                answer.append("\n-----------Found-------------\n")
                answer.append(line)
        answer.append("\n-----------Meaning-------------\n")
        answer.append(getMeaning(substring))
    return '\n'.join(answer)
