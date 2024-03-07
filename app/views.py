from django.http import HttpResponse
from django.shortcuts import render
from django.core.files import File
from app.tools import *
from .models import File
__SOURCE = getPDFContent("app/pdf/lang.pdf")

def homePageView(request):
    print(request.POST)
    print(request.FILES)
    if request.POST:
        if request.POST.get("translate") and request.POST.get("input_text"):
            text = request.POST.get("input_text")
            output_text = algorithm(text)
            return render(request, 'main_page.html', { 'input': text, "output": output_text })  
        if request.POST.get("clear"):
            return render(request, 'main_page.html',  { 'input': None, "output": None }) 
        if request.POST.get("open"):
            file = request.FILES.get("file")
            print("f", file)
            if file:
                text = getPDFContent(file)
                print("text", text)
                return render(request, 'main_page.html', { 'input': text, "output": None }) 
    return render(request, 'main_page.html')
    