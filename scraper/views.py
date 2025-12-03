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
            # Ejemplo: scraping en Wikipedia
            url = f"https://es.wikipedia.org/wiki/{query}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Título de la página
                titulo = soup.find("h1").get_text(strip=True)

                # Snippets: párrafos iniciales
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
