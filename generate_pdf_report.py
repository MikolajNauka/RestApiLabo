"""
Skrypt generujący profesjonalne Sprawozdanie w formacie PDF
z osadzonymi zrzutami ekranu (base64) i pełną dokumentacją zadania.
"""

import os
import base64
import subprocess

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(WORKSPACE_DIR, "screenshots")
OUTPUT_PDF = os.path.join(WORKSPACE_DIR, "Sprawozdanie_System_Rozproszony_REST_API.pdf")
REPORT_HTML_PATH = os.path.join(WORKSPACE_DIR, "report_preview.html")

def get_base64_image(image_filename):
    path = os.path.join(SCREENSHOTS_DIR, image_filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Nie znaleziono pliku obrazu: {path}")
    with open(path, "rb") as f:
        data = f.read()
    return f"data:image/png;base64,{base64.b64encode(data).decode('utf-8')}"

def build_report_html():
    img1 = get_base64_image("01_running_servers.png")
    img2 = get_base64_image("02_success_scenario.png")
    img3 = get_base64_image("03_error_scenario.png")

    html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<title>Sprawozdanie: Budowa systemu rozproszonego z użyciem REST API</title>
<style>
  @page {{
    size: A4;
    margin: 15mm 15mm 15mm 15mm;
  }}
  body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.55;
    font-size: 11pt;
    margin: 0;
    padding: 0;
  }}
  .header {{
    border-bottom: 3px solid #2563eb;
    padding-bottom: 12px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  .header-left h1 {{
    font-size: 18pt;
    color: #0f172a;
    margin: 0 0 6px 0;
    font-weight: 700;
  }}
  .header-left .subtitle {{
    font-size: 11pt;
    color: #475569;
    font-weight: 500;
  }}
  .header-right {{
    text-align: right;
    font-size: 9.5pt;
    color: #64748b;
  }}
  h2 {{
    color: #1e3a8a;
    font-size: 13.5pt;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 5px;
    margin-top: 22px;
    margin-bottom: 12px;
    page-break-after: avoid;
  }}
  h3 {{
    color: #0f172a;
    font-size: 11.5pt;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}
  p {{
    margin: 0 0 10px 0;
    text-align: justify;
  }}
  ul, ol {{
    margin: 0 0 12px 0;
    padding-left: 22px;
  }}
  li {{
    margin-bottom: 4px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 10pt;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 7px 10px;
    text-align: left;
  }}
  th {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
  }}
  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}
  code {{
    font-family: 'Consolas', monospace;
    background: #f1f5f9;
    padding: 1.5px 4.5px;
    border-radius: 4px;
    font-size: 9.5pt;
    color: #0f766e;
  }}
  pre {{
    background: #0f172a;
    color: #f8fafc;
    padding: 12px;
    border-radius: 6px;
    font-family: 'Consolas', monospace;
    font-size: 8.5pt;
    line-height: 1.45;
    overflow-x: auto;
    margin: 8px 0 14px 0;
    page-break-inside: avoid;
  }}
  .badge {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 8.5pt;
    font-weight: 600;
  }}
  .badge-get {{ background: #dbeafe; color: #1d4ed8; }}
  .badge-port {{ background: #f3e8ff; color: #7e22ce; }}
  .card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #2563eb;
    border-radius: 4px;
    padding: 10px 14px;
    margin: 12px 0;
    font-size: 10pt;
  }}
  .diagram-container {{
    text-align: center;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px;
    margin: 14px 0;
  }}
  .screenshot-box {{
    margin: 16px 0 20px 0;
    page-break-inside: avoid;
  }}
  .screenshot-box img {{
    width: 100%;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    display: block;
  }}
  .screenshot-caption {{
    font-size: 9pt;
    color: #475569;
    text-align: center;
    margin-top: 6px;
    font-style: italic;
  }}
  .page-break {{
    page-break-before: always;
  }}
  .repo-box {{
    background: #eff6ff;
    border: 1.5px dashed #3b82f6;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 20px;
    page-break-inside: avoid;
  }}
  .repo-box strong {{
    color: #1e40af;
  }}
</style>
</head>
<body>

  <!-- Nagłówek dokumentu -->
  <div class="header">
    <div class="header-left">
      <h1>Sprawozdanie: System Rozproszony REST API</h1>
      <div class="subtitle">Zadanie: Budowa systemu rozproszonego z użyciem REST API</div>
    </div>
    <div class="header-right">
      <div><strong>Autor:</strong> Mikołaj Marcinkiewicz</div>
      <div><strong>Data:</strong> 14 listopada 2026 r.</div>
      <div><strong>Status:</strong> Zrealizowane (100%)</div>
    </div>
  </div>

  <!-- 1. Cel i Wstęp -->
  <h2>1. Cel zadania i architektura systemu</h2>
  <p>
    Celem niniejszego zadania było praktyczne zaimplementowanie komunikacji między dwoma niezależnymi mikroserwisami
    w architekturze rozproszonej przy użyciu protokołu <strong>REST (Representational State Transfer)</strong> przez HTTP.
    System realizuje wspólny proces biznesowy: Serwis Magazynowy udostępnia informacje o stanach magazynowych towarów,
    lecz przed udzieleniem odpowiedzi synchronicznie odpytuje Serwis Produktów o potwierdzenie istnienia danego produktu.
  </p>

  <div class="diagram-container">
    <svg width="680" height="150" viewBox="0 0 680 150" xmlns="http://www.w3.org/2000/svg">
      <!-- Klient -->
      <rect x="10" y="35" width="130" height="80" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
      <text x="75" y="70" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#1e3a8a" text-anchor="middle">KLIENT REST</text>
      <text x="75" y="90" font-family="'Segoe UI', sans-serif" font-size="10" fill="#475569" text-anchor="middle">(cURL / Postman / UI)</text>

      <!-- Strzałka 1 -->
      <path d="M 140 75 L 230 75" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)"/>
      <text x="185" y="65" font-family="'Segoe UI', sans-serif" font-size="9" fill="#1d4ed8" text-anchor="middle" font-weight="600">GET /stock/{{id}}</text>

      <!-- Serwis Magazynowy -->
      <rect x="230" y="25" width="180" height="100" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
      <text x="320" y="55" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#14532d" text-anchor="middle">SERWIS MAGAZYNOWY</text>
      <text x="320" y="75" font-family="'Segoe UI', sans-serif" font-size="10" fill="#15803d" text-anchor="middle">Port 8002</text>
      <text x="320" y="95" font-family="'Segoe UI', sans-serif" font-size="9" fill="#4b5563" text-anchor="middle">Weryfikuje istnienie produktu</text>
      <text x="320" y="110" font-family="'Segoe UI', sans-serif" font-size="9" fill="#4b5563" text-anchor="middle">w Serwisie Produktów</text>

      <!-- Strzałka 2 -->
      <path d="M 410 75 L 490 75" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow)"/>
      <text x="450" y="65" font-family="'Segoe UI', sans-serif" font-size="9" fill="#15803d" text-anchor="middle" font-weight="600">GET /products/{{id}}</text>

      <!-- Serwis Produktów -->
      <rect x="490" y="25" width="180" height="100" rx="8" fill="#faf5ff" stroke="#9333ea" stroke-width="2"/>
      <text x="580" y="55" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#581c87" text-anchor="middle">SERWIS PRODUKTÓW</text>
      <text x="580" y="75" font-family="'Segoe UI', sans-serif" font-size="10" fill="#7e22ce" text-anchor="middle">Port 8001</text>
      <text x="580" y="95" font-family="'Segoe UI', sans-serif" font-size="9" fill="#4b5563" text-anchor="middle">Katalog produktów</text>
      <text x="580" y="110" font-family="'Segoe UI', sans-serif" font-size="9" fill="#4b5563" text-anchor="middle">(ID, nazwa, cena)</text>

      <!-- Grot strzałki -->
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"/>
        </marker>
      </defs>
    </svg>
    <div style="font-size: 8.5pt; color: #64748b; margin-top: 4px;">Rysunek 1: Przepływ synchronicznej komunikacji HTTP/REST między mikroserwisami.</div>
  </div>

  <h2>2. Kontrakt API obu mikroserwisów</h2>
  <p>Zaprojektowano i zaimplementowano następujące kontrakty REST:</p>
  <table>
    <thead>
      <tr>
        <th>Mikroserwis</th>
        <th>Metoda i Endpoint</th>
        <th>Przykładowa odpowiedź (200 OK)</th>
        <th>Obsługa błędu (404)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Serwis Produktów</strong><br><span class="badge badge-port">Port 8001</span></td>
        <td><span class="badge badge-get">GET</span> <code>/products/&#123;id&#125;</code></td>
        <td><code>&#123; "id": 101, "name": "Laptop Dell XPS 15", "price": 7499.99 &#125;</code></td>
        <td><code>404 Not Found</code>:<br><code>&#123; "detail": "Produkt o ID 999 nie został znaleziony." &#125;</code></td>
      </tr>
      <tr>
        <td><strong>Serwis Magazynowy</strong><br><span class="badge badge-port">Port 8002</span></td>
        <td><span class="badge badge-get">GET</span> <code>/stock/&#123;productId&#125;</code></td>
        <td><code>&#123; "productId": 101, "quantity": 15 &#125;</code></td>
        <td><code>404 Not Found</code>:<br><code>&#123; "detail": "Produkt o ID 999 nie istnieje w Serwisie Produktów." &#125;</code></td>
      </tr>
    </tbody>
  </table>

  <h2>3. Implementacja technologiczna</h2>
  <p>
    Do realizacji zadania wybrano język <strong>Python 3</strong> oraz nowoczesny, asynchroniczny framework <strong>FastAPI</strong>
    uruchamiany na serwerze <strong>Uvicorn</strong>:
  </p>
  <ul>
    <li><strong>Serwis Produktów:</strong> Przechowuje mockowaną kolekcję encji <code>Product</code> w pamięci RAM. Udostępnia endpoint <code>GET /products/{{id}}</code>, weryfikuje obecność klucza w słowniku i zwraca model JSON lub rzuca wyjątek <code>HTTPException(status_code=404)</code>.</li>
    <li><strong>Serwis Magazynowy:</strong> Używa biblioteki <code>requests</code> z ustawionym limitem czasu (timeout) do wykonania zapytania GET do Serwisu Produktów pod adresem <code>http://127.0.0.1:8001/products/{{product_id}}</code>. Jeśli serwis zwróci status 200, Serwis Magazynowy odczytuje stan magazynowy z bazy <code>STOCK_DB</code>. Jeśli zwróci kod 404, Serwis Magazynowy natychmiast propaguje błąd 404 do klienta. Dodatkowo zaimplementowano obsługę błędu <code>503 Service Unavailable</code> w sytuacji braku łączności sieciowej.</li>
  </ul>

  <!-- Nowa strona dla zrzutów ekranu -->
  <div class="page-break"></div>

  <h2>4. Weryfikacja działania i zrzuty ekranu</h2>
  <p>
    Zgodnie z wymaganiami zadania wykonano weryfikację działania systemu w trzech kluczowych scenariuszach:
  </p>

  <!-- Screenshot 1 -->
  <div class="screenshot-box">
    <h3>4.1. Zrzut ekranu odpalonych obu serwerów</h3>
    <p>Obydwa mikroserwisy pracują jako w pełni niezależne procesy w oddzielnych terminalach, nasłuchując na portach 8001 i 8002:</p>
    <img src="{img1}" alt="Zrzut ekranu uruchomionych serwerów">
    <div class="screenshot-caption">Rysunek 2: Równoległe uruchomienie Serwisu Produktów (port 8001) oraz Serwisu Magazynowego (port 8002).</div>
  </div>

  <!-- Screenshot 2 -->
  <div class="screenshot-box">
    <h3>4.2. Zrzut ekranu scenariusza sukcesu (Produkt istnieje)</h3>
    <p>
      Zapytanie klienta pod adres <code>http://localhost:8002/stock/101</code>. Serwis Magazynowy potwierdza obecność produktu
      w Serwisie Produktów i zwraca stan <code>quantity: 15</code> ze statusem <strong>HTTP 200 OK</strong>:
    </p>
    <img src="{img2}" alt="Zrzut ekranu scenariusza sukcesu">
    <div class="screenshot-caption">Rysunek 3: Pomyślna komunikacja między-serwisowa w scenariuszu sukcesu (HTTP 200 OK).</div>
  </div>

  <!-- Nowa strona dla zrzutu błędu i podsumowania -->
  <div class="page-break"></div>

  <!-- Screenshot 3 -->
  <div class="screenshot-box">
    <h3>4.3. Zrzut ekranu scenariusza błędu (Produkt nie istnieje)</h3>
    <p>
      Zapytanie klienta o nieistniejący produkt (ID: 999) pod adres <code>http://localhost:8002/stock/999</code>.
      Serwis Produktów zwraca kod 404, a Serwis Magazynowy poprawnie przechwytuje tę odpowiedź i propaguje kod
      <strong>HTTP 404 Not Found</strong> z czytelnym komunikatem błędu:
    </p>
    <img src="{img3}" alt="Zrzut ekranu scenariusza błędu">
    <div class="screenshot-caption">Rysunek 4: Poprawna propagacja błędu 404 Not Found w przypadku braku zasobu.</div>
  </div>

  <h2>5. Podsumowanie i wnioski</h2>
  <div class="card">
    <strong>Główne wnioski z realizacji zadania:</strong>
    <ol style="margin-top: 6px; margin-bottom: 0;">
      <li><strong>Separacja odpowiedzialności (Separation of Concerns):</strong> Podział domeny biznesowej na katalog produktów i stan magazynowy pozwala na niezależny rozwój, skalowanie i wdrażanie każdego z modułów.</li>
      <li><strong>Standaryzacja protokołu REST:</strong> Wykorzystanie kodów stanu HTTP (200, 404, 503) oraz formatu JSON gwarantuje jednoznaczność interpretacji odpowiedzi przez systemy integrujące.</li>
      <li><strong>Odporność na błędy:</strong> Kluczowym elementem systemów rozproszonych jest poprawna obsługa sytuacji awaryjnych (propagacja kodów błędów oraz obsługa niedostępności serwisów zależnych z użyciem mechanizmu timeout).</li>
    </ol>
  </div>

  <h2>6. Repozytorium kodu na GitHub</h2>
  <div class="repo-box">
    <strong>Link do repozytorium GitHub projektu:</strong><br>
    <span style="font-size: 11pt; font-family: 'Consolas', monospace; color: #1e3a8a;">
      https://github.com/MikolajNauka/restapi
    </span>
    <p style="margin-top: 8px; font-size: 9.5pt; color: #334155;">
      Repozytorium zawiera pełny kod źródłowy obu serwisów, skrypt testowy, konfigurację środowiska (<code>requirements.txt</code>),
      skrypty uruchomieniowe (<code>.bat</code> i <code>.py</code>) oraz niniejszą dokumentację PDF.
    </p>
  </div>

</body>
</html>
"""
    return html

def main():
    print("Budowanie dokumentu HTML...")
    html_content = build_report_html()
    with open(REPORT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Zapisano plik podglądu HTML: {REPORT_HTML_PATH}")

    print("Kompilowanie do pliku PDF przez Microsoft Edge...")
    powershell_cmd = f'& "{EDGE_PATH}" --headless=new --disable-gpu --no-sandbox --print-to-pdf="{OUTPUT_PDF}" --no-pdf-header-footer "file:///{REPORT_HTML_PATH.replace(os.sep, "/")}"'
    subprocess.run(["powershell", "-NoProfile", "-Command", powershell_cmd], check=False)
    if os.path.exists(OUTPUT_PDF):
        print(f"Sukces! Wygenerowano plik PDF: {OUTPUT_PDF}")
    else:
        print(f"Uwaga: Plik HTML został wygenerowany ({REPORT_HTML_PATH}). W razie potrzeby można otworzyć go w przeglądarce i zapisać jako PDF (Drukuj -> Zapisz jako PDF).")

if __name__ == "__main__":
    main()
