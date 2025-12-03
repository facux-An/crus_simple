import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

# ---------- Scrapers por fuente ----------

def scrape_wikipedia(query: str):
    url = f"https://es.wikipedia.org/wiki/{query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=8)

    if resp.status_code != 200:
        return [], f"No se pudo acceder a {url} (status {resp.status_code})"

    soup = BeautifulSoup(resp.text, "html.parser")
    titulo_el = soup.find("h1")
    titulo = titulo_el.get_text(strip=True) if titulo_el else query

    parrafos = soup.select("p")
    snippets = [p.get_text(strip=True) for p in parrafos[:3] if p.get_text(strip=True)]

    return [{
        "titulo": titulo,
        "snippets": snippets,
        "url": url,
    }], None

###############################################################################
def _extraer_productos_de_contents(contents, limit=20):
    """
    Recorre blocks en contents y extrae productos desde records → attributes.
    Retorna una lista de dicts {titulo, precio, marca, url}.
    """
    resultados = []
    for bloque in contents:
        records = bloque.get("records", [])
        for r in records:
            attrs = r.get("attributes", {})
            titulo = (attrs.get("product.displayName") or attrs.get("sku.displayName") or [""]).pop(0).strip() if (attrs.get("product.displayName") or attrs.get("sku.displayName")) else None
            precio_raw = (attrs.get("sku.referencePrice") or attrs.get("sku.activePrice") or [""]).pop(0) if (attrs.get("sku.referencePrice") or attrs.get("sku.activePrice")) else None
            marca = (attrs.get("product.brand") or [""]).pop(0)

            detalle = r.get("detailsAction", {}).get("recordState", "")
            url_detalle = f"https://www.cotodigital.com.ar/sitios/cdigi{detalle}" if detalle else None

            if titulo:
                # Normalizar precio a string legible
                try:
                    precio = f"{float(str(precio_raw).replace(',', '.')):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                except Exception:
                    precio = precio_raw or "No disponible"

                resultados.append({
                    "titulo": titulo,
                    "precio": precio,
                    "marca": marca,
                    "url": url_detalle,
                })
                if len(resultados) >= limit:
                    return resultados
    return resultados


def scrape_coto(query: str):
    """
    Busca productos en Coto Digital usando browse?Ntt=query&format=json.
    Aplica un fallback con sort por relevancia si la primera respuesta no trae records.
    """
    base = "https://www.cotodigital.com.ar/sitios/cdigi/browse"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
    }

    # 1) Intento principal con Ntt
    url_1 = f"{base}?Ntt={query}&format=json"
    try:
        resp = requests.get(url_1, headers=headers, timeout=12)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return [], f"Error consultando Coto: {e}"

    contents = data.get("contents") or data.get("Main") or []
    resultados = _extraer_productos_de_contents(contents, limit=24)

    # 2) Fallback si no hay productos: forzar orden por relevancia (Ns)
    if not resultados:
        url_2 = f"{base}?Ntt={query}&Ns=product.RELEVANCIA|0&format=json"
        try:
            resp2 = requests.get(url_2, headers=headers, timeout=12)
            resp2.raise_for_status()
            data2 = resp2.json()
            contents2 = data2.get("contents") or data2.get("Main") or []
            resultados = _extraer_productos_de_contents(contents2, limit=24)
        except Exception:
            pass

    # 3) Mensaje si sigue vacío
    if not resultados:
        return [], "No se encontraron productos para tu búsqueda en Coto."

    return resultados, None

############################################################################################
def scraper_view(request):
    """
    Vista principal del scraper.
    Recibe ?q=termino y muestra resultados de Coto Digital.
    """
    query = request.GET.get("q", "")
    resultados, error = scrape_coto(query) if query else ([], None)

    context = {
        "query": query,
        "resultados": resultados,
        "error": error,
    }
    return render(request, "scraper.html", context)


def scrape_local(query: str):
    try:
        with open("scraper/static/local.html", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
    except Exception as e:
        return [], f"No se pudo leer el HTML local: {e}"

    titulo_el = soup.find("title")
    titulo = titulo_el.get_text(strip=True) if titulo_el else f"Local: {query}"

    parrafos = soup.select("p")
    snippets = [p.get_text(strip=True) for p in parrafos[:3] if p.get_text(strip=True)]

    return [{
        "titulo": titulo,
        "snippets": snippets,
        "url": "local.html",
    }], None


# ---------- Vistas ----------

def home_scraper(request):
    return render(request, "scraper/scraper.html")


def buscar(request):
    query = request.GET.get("q", "").strip()
    source = request.GET.get("source", "wikipedia")  # por defecto Wikipedia
    resultados, error = [], None

    if query:
        try:
            if source == "wikipedia":
                resultados, error = scrape_wikipedia(query)
            elif source == "coto":
                resultados, error = scrape_coto(query)
            elif source == "local":
                resultados, error = scrape_local(query)
            else:
                error = "Fuente desconocida."
        except Exception as e:
            error = f"Error al hacer scraping: {e}"

    context = {
        "query": query,
        "source": source,
        "resultados": resultados,
        "error": error,
    }
    return render(request, "scraper/scraper.html", context)
