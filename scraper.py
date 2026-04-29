import requests
from bs4 import BeautifulSoup
import sys
import time
from rdf_builder import buat_rdf

sys.stdout.reconfigure(encoding="utf-8")
HEADERS = {"User-Agent": "Mozilla/5.0"}

def ambil_tanggal_antara(url_artikel):
    try:
        soup = BeautifulSoup(requests.get(url_artikel, headers=HEADERS).text, "html.parser")
        span = soup.find("span", class_=["text-secondary", "font-weight-normal"])
        if span:
            if span:
                for i in span.find_all("i"):
                    i.decompose()
                return span.get_text(strip=True)
    except:
        pass
    return "-"

def ambil_tanggal_cnn(url_artikel):
    try:
        soup = BeautifulSoup(requests.get(url_artikel, headers=HEADERS).text, "html.parser")
        div = soup.find("div", class_="text-cnn_grey text-sm mb-4")
        if div:
            return div.get_text(strip=True)
    except:
        pass
    return "-"

#DETIK NEWS
def scrape_detik():
    hasil = []
    page = 1

    while len(hasil) < 25:
        url = "https://www.detik.com/search/searchall?query=politik&siteid=3&source_kanal=true"
        soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
        articles = soup.find_all("div", class_="media__text")

        if not articles:
            break
        for article in articles:
            if len(hasil) >= 25:
                break

            judul_tag   = article.find("h3", class_="media__title")
            link_tag    = article.find("a", class_="media__link")
            tanggal_tag = article.find("div", class_="media__date")

            if judul_tag and link_tag:
                span = tanggal_tag.find("span") if tanggal_tag else None
                hasil.append({
                    "judul"   : judul_tag.get_text(strip=True),
                    "url"     : link_tag["href"],
                    "tanggal" : span["title"] if span else "-",
                    "sumber"  : "Detik News",
                    "kategori": "Politik"
                })
        page += 1
    return hasil

#KOMPAS
def scrape_kompas():
    hasil = []
    page = 1

    while len(hasil) < 25:
        url = "https://search.kompas.com/search?q=politik"
        soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
        articles = soup.find_all("div", class_="articleItem")

        if not articles:
            break
        for article in articles:
            if len(hasil) >= 25:
                break

            judul_tag   = article.find("h2", class_="articleTitle")
            link_tag    = article.find("a", class_="article-link")
            tanggal_tag = article.find("div", class_="articlePost-date")

            if judul_tag and link_tag:
                hasil.append({
                    "judul"   : judul_tag.get_text(strip=True),
                    "url"     : link_tag["href"],
                    "tanggal" : tanggal_tag.get_text(strip=True),
                    "sumber"  : "Kompas",
                    "kategori": "Politik"
                })
        page += 1
    return hasil

#ANTARA NEWS
def scrape_antara():
    hasil = []
    page = 1

    while len(hasil) < 25:
        url = f"https://www.antaranews.com/politik?page={page}"
        soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
        articles = soup.find_all("h2", class_="post_title")

        if not articles:
            break

        for h2 in articles:
            if len(hasil) >= 25:
                break

            link_tag = h2.find("a", href=True)
            if not link_tag:
                continue

            judul = link_tag.get("title") or link_tag.get_text(strip=True)
            url_artikel = link_tag["href"]

            tanggal = ambil_tanggal_antara(url_artikel)
            time.sleep(0.5)  #jeda agar tidak diblokir

            hasil.append({
                "judul"    : judul,
                "url"      : url_artikel,
                "tanggal"  : tanggal,
                "sumber"   : "Antara News",
                "kategori" : "Politik"
            })

        page += 1

    return hasil

#REPUBLIKA
def scrape_republika():
    hasil = []
    page = 1

    while len(hasil) < 25:
        url = "https://republika.co.id/search/v3/?q=politik"
        soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
        articles = soup.find_all("div", class_="news-item")

        if not articles:
            break
        for article in articles:
            if len(hasil) >= 25:
                break

            judul_tag   = article.find("div", class_="news-title")
            link_tag    = article.find("a", href=True)
            tanggal_tag = article.find("div", class_="news-source")

            if judul_tag and link_tag:
                hasil.append({
                    "judul"   : judul_tag.get_text(strip=True),
                    "url"     : link_tag["href"],
                    "tanggal" : tanggal_tag.get_text(strip=True),
                    "sumber"  : "Republika",
                    "kategori": "Politik"
                })
        page += 1
    return hasil

#CNN INDONESIA
def scrape_cnn():
    hasil = []
    page = 1

    while len(hasil) < 25:
        url = f"https://www.cnnindonesia.com/nasional?page={page}"
        soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")

        articles = soup.find_all("article")

        if not articles:
            break

        for article in articles:
            if len(hasil) >= 25:
                break

            judul_tag = article.find("h2", class_=lambda c: c and "text-cnn_black_light" in c)
            link_tag  = article.find("a", href=True)

            if judul_tag and link_tag:
                url_artikel = link_tag["href"]
                tanggal = ambil_tanggal_cnn(url_artikel)
                time.sleep(0.5)

                hasil.append({
                    "judul"    : judul_tag.get_text(strip=True),
                    "url"      : url_artikel,
                    "tanggal"  : tanggal,
                    "sumber"   : "CNN Indonesia",
                    "kategori" : "Politik"
                })

        page += 1

    return hasil

def scrape_semua():
    semua = []

    sumber = [
        ("Detik News", scrape_detik),
        ("Kompas", scrape_kompas),
        ("Antara News",   scrape_antara),
        ("Republika",     scrape_republika),
        ("CNN Indonesia",         scrape_cnn),
    ]

    for nama, fungsi in sumber:
        try:
            data = fungsi()
            semua.extend(data)
            print(f"{nama}: {len(data)} berita")
        except Exception as e:
            print(f"x {nama} gagal: {e}")
    
    return semua


data = scrape_semua()
print(f"\nTotal keseluruhan: {len(data)} berita")

# Konversi ke RDF dan simpan ke file .ttl
buat_rdf(data)