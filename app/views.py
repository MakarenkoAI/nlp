from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files import File
from app.tools import *
from .models import File

__INPUT = None
__OUTPUT = None

def homePageView(request):
    global __INPUT
    global __OUTPUT
 
    if request.method == 'POST':
        if request.POST.get("translate") and request.POST.get("input_text"):
            __INPUT = request.POST.get("input_text")
            __OUTPUT = algorithm(__INPUT)
            return render(request, 'main_page.html', {'input': __INPUT, "output": __OUTPUT})  
        if request.POST.get("clear"):
            return render(request, 'main_page.html',  {'input': None, "output": None}) 
        if request.POST.get("open"):
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
            text='helptext'
            return render(request, 'main_page.html', {'help_text': text})
        if request.POST.get("dictionary"):  
            return redirect('dictionary')
        

        if request.POST.get("searchdict"):
            substring = request.POST.get("searchdict")
            print(substring)
            lines = findLines(substring)
            print(lines)
            return render(request, 'dictionary.html', {'text': lines})
        if request.POST.get("savedict"):
            text = request.POST.get("dict_text")
            print(text)
            text = writeInFile(text)
            return render(request, 'dictionary.html', {'text': text})
        if request.POST.get("cleardict"):
            clearFile()
            return render(request, 'dictionary.html')
        if request.POST.get("return"):
            return render(request, 'main_page.html',  { 'input': __INPUT, "output": __OUTPUT})
        
        
    return render(request, 'main_page.html')
    
def dictPageView(request):
    text = ''
    with open("dictionary.txt", 'r') as file:
        text = file.read()
    return render(request, 'dictionary.html', {'text': text})

def writeInFile(output:str)->str :
    with open("dictionary.txt", "r") as file:
        text = file.read()
        print(text)
        text = text.split('\n')
        text += output.split('\r\n')
        text = list(set(text))
        print(text)
        with open("dictionary.txt", "w") as fileW:
            text = '\n'.join(sorted(text))
            print(text)
            fileW.write(text)
    return text

def clearFile():
    with open("dictionary.txt", "w") as file:
       file.write("")

def findLines(substring:str)-> str:
    answer = []
    with open("dictionary.txt", "r") as file:
        text = file.read()
        text = text.split('\n')
        if substring == '.': return '\n'.join(text)
        for line in text:
            if substring in line:
                answer.append(line)
    return '\n'.join(answer)