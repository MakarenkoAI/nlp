from django.shortcuts import render, redirect
from app.tools import *
from app.syntax_analysis import *
from app.script import *
from django.http import HttpResponse
from bs4 import BeautifulSoup as Soup
from fpdf import FPDF
import textwrap

__INPUT = None
__OUTPUT = None
__HISTORY = []

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
        writeInFile(__OUTPUT, "dictionary.txt")
        return render(request, 'main_page.html', { 'input': __INPUT, "output": __OUTPUT}) 
    if request.POST.get("saveD") and request.POST.get("input_text"):
        __INPUT = request.POST.get("input_text")
        writeInDialog(__INPUT, "dialog.pdf")
        return render(request, 'main_page.html', { 'input': __INPUT, "output": __OUTPUT}) 
    
    if request.POST.get("dictionary"):  
        return redirect('dictionary')
    
    if request.POST.get("chat"):  
        return redirect('chat')
        
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
        writeInFile(text, "dictionary.txt")
        return render(request, 'dictionary.html', {'text': text})
    if request.POST.get("return") == 'Return':
        return redirect('home')
    if request.POST.get("cleardict"):
        clearFile()
        return render(request, 'dictionary.html')

class objecT():
    def __init__(self, answer, inputtext):
        self.first = inputtext
        self.second = answer

def chatPageView(request):
    chat = J2ChatAI()
    global __HISTORY
    print(request.POST)
    if request.POST.get("return") == 'Return':
        return redirect('home')
    if request.POST.get("Send") and request.POST.get("inputtext"):
        inputtext = request.POST.get("inputtext")
        messages[1]['text'] = inputtext
        response = chat.make_request_to_chat(messages, model_description)
        answer = str(response['outputs'][0]['text'])
        v = objecT(answer, inputtext)
        __HISTORY.insert(0, v)
        return render(request, 'chat.html', {'items': __HISTORY})
    if request.POST.get("save"):
        text = ''
        for el in reversed(__HISTORY):
            text += f'User: {el.first}\n'
            text += f'Bookie: {el.second}\n'
        writeInDialog(text, "dialog.pdf")
        return render(request, 'chat.html', {'items': __HISTORY})
    return render(request, 'chat.html',  {'items': __HISTORY})
    
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

def writeInDialog(text:str, filename) :
    # pdf = FPDF()
    # pdf.add_page()
    # pdf.set_font("Arial", size = 14)
    # pdf.cell(200, 10, txt = output, align = 'C')
    # pdf.output(filename)   
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')

def writeInFile(output:str, filename) :
    rez = ''
    with open(filename, "r", encoding="utf-8") as fileW:
        text = fileW.read()
        output = get_lines(output)
        print(output)
        for el in output:
            if el not in text:
                rez += '\n' + el
    with open(filename, "w", encoding="utf-8") as file:
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
