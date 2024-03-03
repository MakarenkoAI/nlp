from django.http import HttpResponse
from django.shortcuts import render

def homePageView(request):
    return render(request, 'main_page.html')
    
    # return HttpResponse('html/main_page.html')