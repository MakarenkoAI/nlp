from django.shortcuts import render, redirect
from app.tools import *

__INPUT = None
__OUTPUT = None

def homePageView(request):
    global __INPUT
    global __OUTPUT
    print(request.POST)
    if request.method == 'POST':
        if request.POST.get("translate") and request.POST.get("input_text"):
            __INPUT = request.POST.get("input_text")
            __OUTPUT = algorithm2(__INPUT)
            return render(request, 'main_page.html', {'input': __INPUT, "output": __OUTPUT})  
        
        if request.POST.get("clear"):
            return render(request, 'main_page.html',  {'input': None, "output": None}) 
        
        if  request.POST.get("open"):
            file = request.FILES.get("file")
            if file:
                __INPUT = getPDFContent(file)
                return render(request, 'main_page.html', { 'input': __INPUT, "output": None }) 
            
        if request.POST.get("save") and request.POST.get("output_text"):
            __INPUT = request.POST.get("input_text")
            __OUTPUT = request.POST.get("output_text")
            writeInFile(__OUTPUT)
            return render(request, 'main_page.html', { 'input': __INPUT, "output": __OUTPUT}) 
        
        if request.POST.get("help"):
            writeInFile(__OUTPUT)
            return render(request, 'main_page.html', { 'input': __INPUT, "output": __OUTPUT}) 
        
        if request.POST.get("dictionary"):  
            return redirect('dictionary')
        
        if request.POST.get("savedict") != None:
            text = request.POST.get("dict_text")
            text = writeInFile(text)
            return render(request, 'dictionary.html', {'text': text})
        
        if request.POST.get("return") != None:
            return render(request, 'main_page.html',  { 'input': __INPUT, "output": __OUTPUT})
        
        if request.POST.get("searchdict") != "":
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

def writeInFile(output:str)->str :
    with open("dictionary.txt", "r", encoding="utf-8") as file:
        text = file.read()
        text = text.split('\n')
        sents = []
        for line in text:  sents.append([nltk.word_tokenize(line), line])
        text2 = output.split('\r\n')
        sents2 = []
        for line in text2: sents2.append([nltk.word_tokenize(line), line])
        new = [line[1] for line in sents2]
        for line2 in sents2:
            if line2[0]:
                for line in sents:
                    if line[0]:
                        if line[0][0] != line2[0][0]:
                            new.append(line[1])
        text = list(set(new))
        with open("dictionary.txt", "w", encoding="utf-8") as fileW:
            text = '\n'.join(sorted(text))
            fileW.write(text)
    return text

def clearFile():
    with open("dictionary.txt", "w", encoding="utf-8") as file:
       file.write("")

def findLines(substring:str)-> str:
    answer = []
    with open("dictionary.txt", "r", encoding="utf-8") as file:
        text = file.read()
        text = text.split('\n')
        if substring == '.': return '\n'.join(text)
        for line in text:
            if substring in line:
                answer.append(line)
    return '\n'.join(answer)
