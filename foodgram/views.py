from django.shortcuts import render


def page_not_found(request, exception):
    """ View-функция для отображения страницы с ошибкой 404 """
    return render(request, "404.html", status=404)


def server_error(request):
    """ View-функция для отображения страницы с ошибкой 500 """
    return render(request, "500.html", status=500) 


def about_author(request):
    """ View-функция для отображения страницы "Об авторе" """
    return render(request, "flatpages/about_author.html")


def about_foodgram(request):
    """ View-функция для отображения страницы с "Продуктовый помощник" """
    return render(request, "flatpages/about_foodgram.html")


def about_tech(request):
    """ View-функция для отображения страницы с "Технологии" """
    return render(request, "flatpages/about_tech.html")
