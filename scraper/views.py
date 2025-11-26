from django.shortcuts import render

def scrape_view(request):
    return render(request, "scraper/scrape.html")
