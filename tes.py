# Untuk verifikasi bisa ambil data di paginasi selanjutntya
# import requests
# from bs4 import BeautifulSoup

# HEADERS = {"User-Agent": "Mozilla/5.0"}

# # Detik pakai parameter 'page' untuk pagination
# for page in range(1, 4):  # coba 3 halaman dulu
#     url = f"https://www.detik.com/search/searchall?query=politik&siteid=3&source_kanal=true&page={page}"
#     response = requests.get(url, headers=HEADERS)
#     soup = BeautifulSoup(response.text, "html.parser")
#     items = soup.find_all("div", class_="media__text")
#     print(f"Halaman {page}: {len(items)} berita")

# Untuk verifikasi bisa mengambil datanya dgn tepat
# import requests
# from bs4 import BeautifulSoup

# HEADERS = {"User-Agent": "Mozilla/5.0"}
# url = "https://www.detik.com/search/searchall?query=politik&siteid=3&source_kanal=true"

# response = requests.get(url, headers=HEADERS)
# soup = BeautifulSoup(response.text, "html.parser")

# # Cek apakah halaman berhasil dimuat
# print("Status:", response.status_code)

# # Cek berapa banyak div media__text yang ditemukan
# items = soup.find_all("div", class_="media__text")
# print("Jumlah item ditemukan:", len(items))

# # Lihat isi HTML item pertama (kalau ada)
# if items:
#     print("\nHTML item pertama:")
#     print(items[0].prettify())
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

url_test = "https://www.tempo.co/politik/prabowo-akan-nyanyikan-lagu-internasionale-bersama-buruh-di-may-day-2026-2132613"
soup = BeautifulSoup(requests.get(url_test, headers=HEADERS).text, "html.parser")

# Cari semua elemen yang mengandung tanggal
print("Cari teks mengandung 'April' atau 'WIB' atau '2026':")
for tag in soup.find_all(["span", "p", "div", "time"]):
    teks = tag.get_text(strip=True)
    if any(k in teks for k in ["WIB", "2026", "April"]):
        print(f"tag: {tag.name} | class: {tag.get('class')} | teks: {teks[:80]}")