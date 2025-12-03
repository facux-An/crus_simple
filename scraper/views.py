import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

def home_scraper(request):
    return render(request, "scraper/scraper.html")

def buscar(request):
    query = request.GET.get("q", "").strip()
    resultados = []
    error = None

    if query:
        try:
            url = f"https://es.wikipedia.org/wiki/{query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                titulo = soup.find("h1").get_text(strip=True)
                parrafos = soup.select("p")
                snippets = [p.get_text(strip=True) for p in parrafos[:3]]

                resultados.append({
                    "titulo": titulo,
                    "snippets": snippets,
                    "url": url,
                })
            else:
                error = f"No se pudo acceder a {url} (status {response.status_code})"

        except Exception as e:
            error = f"Error al hacer scraping: {e}"

    context = {
        "query": query,
        "resultados": resultados,
        "error": error,
    }
    return render(request, "scraper/buscar.html", context)
