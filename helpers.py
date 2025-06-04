import requests
from bs4 import BeautifulSoup
from transformers import pipeline


def resumir(texto):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    resumo = summarizer(texto, max_length=100, min_length=30, do_sample=False)
    return resumo[0]['summary_text']


def traduzir(texto):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": texto, "langpair": "en|pt"}
    response = requests.get(url, params=params).json()
    return response['responseData']['translatedText']


def gerar_clipping():
    urls = [
        "https://www.bbc.com/news",
        "https://www.cnn.com/world",
        "https://www.g1.globo.com",
    ]

    noticias = []

    for url in urls:
        try:
            pagina = requests.get(url)
            soup = BeautifulSoup(pagina.content, "html.parser")
            titulos = soup.find_all("h3")[:3]

            for titulo in titulos:
                texto = titulo.get_text()
                link = titulo.find_parent("a")["href"] if titulo.find_parent("a") else url

                if not texto:
                    continue

                resumo = resumir(texto)
                if url != "https://www.g1.globo.com":
                    texto = traduzir(texto)
                    resumo = traduzir(resumo)

                noticias.append({
                    "titulo": texto,
                    "resumo": resumo,
                    "link": link
                })
        except Exception as e:
            print(f"Erro ao processar {url}: {e}")

    return noticias
