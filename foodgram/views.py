from django.shortcuts import render

def about_author(request):
    return render(request, 'flatpages/about_author.html')

def about_foodgram(request):
    return render(request, 'flatpages/about_foodgram.html')

def about_tech(request):
    return render(request, 'flatpages/about_tech.html')