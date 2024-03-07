from django.http import HttpResponse
from django.shortcuts import render
from django.core.files import File
from app.tools import *

__SOURCE = getPDFContent("app/Harry_Potter/lang.pdf")

def homePageView(request):
    if request.method == "POST":
        if request.POST.get("input_text") != None:
            text = request.POST.get("input_text")
            output_text = algorithm(text)
            return render(request, 'main_page.html', { 'input': text, "output": output_text }) 
        if request.POST.get("clear") != None:
            return render(request, 'main_page.html') 
        if request.POST.get("open") != None:
            return render(request, 'main_page.html', {'input': __SOURCE}) 
    return render(request, 'main_page.html', {'input': __SOURCE})
    