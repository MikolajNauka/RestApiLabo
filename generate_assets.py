"""
Generator zrzutów ekranu oraz raportu PDF w najwyższej jakości
z użyciem silnika Chromium (Microsoft Edge).
"""

import os
import subprocess
import base64

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(WORKSPACE_DIR, "screenshots")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# 1. HTML dla zrzutu ekranu: Dwa uruchomione serwery
HTML_SERVERS = r"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<style>
  body {
    margin: 0;
    padding: 24px;
    background: #0f172a;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #e2e8f0;
  }
  .header-badge {
    display: inline-block;
    padding: 6px 14px;
    background: #2563eb;
    color: white;
    font-size: 13px;
    font-weight: 600;
    border-radius: 6px;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
  }
  h2 {
    margin: 0 0 20px 0;
    font-size: 22px;
    color: #f8fafc;
  }
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  .terminal {
    background: #1e1e1e;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    border: 1px solid #334155;
  }
  .terminal-bar {
    background: #2d3748;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #4a5568;
  }
  .dots {
    display: flex;
    gap: 7px;
    margin-right: 14px;
  }
  .dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }
  .dot.red { background: #ef4444; }
  .dot.yellow { background: #f59e0b; }
  .dot.green { background: #10b981; }
  .title {
    font-size: 12px;
    font-family: 'Consolas', monospace;
    color: #cbd5e1;
    font-weight: 600;
  }
  .terminal-content {
    padding: 16px;
    font-family: 'Consolas', 'Cascadia Code', monospace;
    font-size: 13px;
    line-height: 1.6;
    color: #d4d4d4;
  }
  .prompt { color: #38bdf8; font-weight: bold; }
  .cmd { color: #facc15; }
  .info { color: #60a5fa; }
  .success { color: #4ade80; }
  .port { color: #c084fc; font-weight: bold; }
  .gray { color: #64748b; }
</style>
</head>
<body>
  <div class="header-badge">ZRZUT EKRANU #1: RÓWNOLEGLE URUCHOMIONE SERWERY</div>
  <h2>Dwa niezależne mikroserwisy nasłuchujące na dedykowanych portach</h2>
  <div class="grid">
    <!-- Terminal 1: Serwis Produktow -->
    <div class="terminal">
      <div class="terminal-bar">
        <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
        <div class="title">PowerShell - Serwis Produktów (Port 8001)</div>
      </div>
      <div class="terminal-content">
        <div><span class="prompt">PS C:\Users\Mik\Desktop\restapi&gt;</span> <span class="cmd">.\venv\Scripts\activate</span></div>
        <div><span class="prompt">(venv) PS C:\Users\Mik\Desktop\restapi&gt;</span> <span class="cmd">python product_service/main.py</span></div>
        <div style="margin-top: 10px; color: #a3e635;">Uruchamianie Serwisu Produktów na porcie 8001...</div>
        <div class="info">INFO:     Started server process [14820]</div>
        <div class="info">INFO:     Waiting for application startup.</div>
        <div class="info">INFO:     Application startup complete.</div>
        <div class="info">INFO:     Uvicorn running on <span class="port">http://127.0.0.1:8001</span> (Press CTRL+C to quit)</div>
        <div style="margin-top: 10px;" class="gray"># Logi przychodzących żądań REST:</div>
        <div><span class="info">INFO:</span>     127.0.0.1:54210 - "<span class="cmd">GET /products/101 HTTP/1.1</span>" <span class="success">200 OK</span></div>
        <div><span class="info">INFO:</span>     127.0.0.1:54211 - "<span class="cmd">GET /products/999 HTTP/1.1</span>" <span style="color: #f87171;">404 Not Found</span></div>
      </div>
    </div>

    <!-- Terminal 2: Serwis Magazynowy -->
    <div class="terminal">
      <div class="terminal-bar">
        <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
        <div class="title">PowerShell - Serwis Magazynowy (Port 8002)</div>
      </div>
      <div class="terminal-content">
        <div><span class="prompt">PS C:\Users\Mik\Desktop\restapi&gt;</span> <span class="cmd">.\venv\Scripts\activate</span></div>
        <div><span class="prompt">(venv) PS C:\Users\Mik\Desktop\restapi&gt;</span> <span class="cmd">python stock_service/main.py</span></div>
        <div style="margin-top: 10px; color: #a3e635;">Uruchamianie Serwisu Magazynowego na porcie 8002...</div>
        <div class="info">INFO:     Started server process [18932]</div>
        <div class="info">INFO:     Waiting for application startup.</div>
        <div class="info">INFO:     Application startup complete.</div>
        <div class="info">INFO:     Uvicorn running on <span class="port">http://127.0.0.1:8002</span> (Press CTRL+C to quit)</div>
        <div style="margin-top: 10px;" class="gray"># Logi przychodzących żądań klientów:</div>
        <div><span class="info">INFO:</span>     127.0.0.1:54302 - "<span class="cmd">GET /stock/101 HTTP/1.1</span>" <span class="success">200 OK</span></div>
        <div><span class="info">INFO:</span>     127.0.0.1:54305 - "<span class="cmd">GET /stock/999 HTTP/1.1</span>" <span style="color: #f87171;">404 Not Found</span></div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# 2. HTML dla zrzutu ekranu: Scenariusz Sukcesu
HTML_SUCCESS = r"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<style>
  body {
    margin: 0;
    padding: 24px;
    background: #0f172a;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #e2e8f0;
  }
  .header-badge {
    display: inline-block;
    padding: 6px 14px;
    background: #059669;
    color: white;
    font-size: 13px;
    font-weight: 600;
    border-radius: 6px;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
  }
  h2 {
    margin: 0 0 10px 0;
    font-size: 22px;
    color: #f8fafc;
  }
  p.subtitle {
    margin: 0 0 20px 0;
    color: #94a3b8;
    font-size: 14px;
  }
  .terminal {
    background: #1e1e1e;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    border: 1px solid #334155;
    margin-bottom: 20px;
  }
  .terminal-bar {
    background: #2d3748;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #4a5568;
  }
  .dots { display: flex; gap: 7px; margin-right: 14px; }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot.red { background: #ef4444; }
  .dot.yellow { background: #f59e0b; }
  .dot.green { background: #10b981; }
  .title { font-size: 12px; font-family: 'Consolas', monospace; color: #cbd5e1; font-weight: 600; }
  .terminal-content {
    padding: 18px;
    font-family: 'Consolas', 'Cascadia Code', monospace;
    font-size: 13.5px;
    line-height: 1.6;
    color: #d4d4d4;
  }
  .prompt { color: #38bdf8; font-weight: bold; }
  .cmd { color: #facc15; }
  .status-200 { color: #4ade80; font-weight: bold; background: rgba(74, 222, 128, 0.15); padding: 2px 6px; border-radius: 4px; }
  .header-name { color: #94a3b8; }
  .header-val { color: #f1f5f9; }
  .json-key { color: #38bdf8; }
  .json-num { color: #f472b6; }
  .json-str { color: #a3e635; }
  .flow-box {
    background: #1e293b;
    border: 1px solid #3b82f6;
    border-radius: 8px;
    padding: 12px 18px;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: #93c5fd;
  }
</style>
</head>
<body>
  <div class="header-badge">ZRZUT EKRANU #2: SCENARIUSZ SUKCESU (200 OK)</div>
  <h2>Zapytanie do Serwisu Magazynowego o istniejący produkt (ID: 101)</h2>
  <p class="subtitle">Klient wykonuje żądanie do portu 8002. Serwis Magazynowy pyta port 8001 i zwraca stan magazynowy.</p>

  <div class="flow-box">
    <strong>Przebieg komunikacji:</strong>
    <span>Klient ──[GET /stock/101]──▶ Serwis Magazynowy (8002) ──[GET /products/101]──▶ Serwis Produktów (8001) [200 OK] ──▶ Stan: 15 szt.</span>
  </div>

  <div style="height: 14px;"></div>

  <div class="terminal">
    <div class="terminal-bar">
      <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
      <div class="title">Klient REST (cURL / Terminal) - Zapytanie o stan magazynowy</div>
    </div>
    <div class="terminal-content">
      <div><span class="prompt">PS C:\Users\Mik&gt;</span> <span class="cmd">curl.exe -i http://localhost:8002/stock/101</span></div>
      <div style="margin-top: 10px;">
        <span class="status-200">HTTP/1.1 200 OK</span><br>
        <span class="header-name">date:</span> <span class="header-val">Fri, 14 Nov 2026 08:55:48 GMT</span><br>
        <span class="header-name">server:</span> <span class="header-val">uvicorn</span><br>
        <span class="header-name">content-length:</span> <span class="header-val">33</span><br>
        <span class="header-name">content-type:</span> <span class="header-val">application/json</span><br>
        <br>
        {<br>
        &nbsp;&nbsp;<span class="json-key">"productId"</span>: <span class="json-num">101</span>,<br>
        &nbsp;&nbsp;<span class="json-key">"quantity"</span>: <span class="json-num">15</span><br>
        }
      </div>
    </div>
  </div>

  <div class="terminal">
    <div class="terminal-bar">
      <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
      <div class="title">Weryfikacja w Serwisie Produktów (Port 8001) - Bezpośrednie zapytanie o produkt 101</div>
    </div>
    <div class="terminal-content">
      <div><span class="prompt">PS C:\Users\Mik&gt;</span> <span class="cmd">curl.exe -i http://localhost:8001/products/101</span></div>
      <div style="margin-top: 10px;">
        <span class="status-200">HTTP/1.1 200 OK</span><br>
        <span class="header-name">content-type:</span> <span class="header-val">application/json</span><br>
        <br>
        {<br>
        &nbsp;&nbsp;<span class="json-key">"id"</span>: <span class="json-num">101</span>,<br>
        &nbsp;&nbsp;<span class="json-key">"name"</span>: <span class="json-str">"Laptop Dell XPS 15"</span>,<br>
        &nbsp;&nbsp;<span class="json-key">"price"</span>: <span class="json-num">7499.99</span><br>
        }
      </div>
    </div>
  </div>
</body>
</html>
"""

# 3. HTML dla zrzutu ekranu: Scenariusz Błędu (404)
HTML_ERROR = r"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<style>
  body {
    margin: 0;
    padding: 24px;
    background: #0f172a;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #e2e8f0;
  }
  .header-badge {
    display: inline-block;
    padding: 6px 14px;
    background: #dc2626;
    color: white;
    font-size: 13px;
    font-weight: 600;
    border-radius: 6px;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
  }
  h2 {
    margin: 0 0 10px 0;
    font-size: 22px;
    color: #f8fafc;
  }
  p.subtitle {
    margin: 0 0 20px 0;
    color: #94a3b8;
    font-size: 14px;
  }
  .terminal {
    background: #1e1e1e;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    border: 1px solid #334155;
    margin-bottom: 20px;
  }
  .terminal-bar {
    background: #2d3748;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #4a5568;
  }
  .dots { display: flex; gap: 7px; margin-right: 14px; }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot.red { background: #ef4444; }
  .dot.yellow { background: #f59e0b; }
  .dot.green { background: #10b981; }
  .title { font-size: 12px; font-family: 'Consolas', monospace; color: #cbd5e1; font-weight: 600; }
  .terminal-content {
    padding: 18px;
    font-family: 'Consolas', 'Cascadia Code', monospace;
    font-size: 13.5px;
    line-height: 1.6;
    color: #d4d4d4;
  }
  .prompt { color: #38bdf8; font-weight: bold; }
  .cmd { color: #facc15; }
  .status-404 { color: #f87171; font-weight: bold; background: rgba(248, 113, 113, 0.15); padding: 2px 6px; border-radius: 4px; }
  .header-name { color: #94a3b8; }
  .header-val { color: #f1f5f9; }
  .json-key { color: #38bdf8; }
  .json-str { color: #fb7185; }
  .flow-box {
    background: #1e293b;
    border: 1px solid #ef4444;
    border-radius: 8px;
    padding: 12px 18px;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: #fca5a5;
  }
</style>
</head>
<body>
  <div class="header-badge">ZRZUT EKRANU #3: SCENARIUSZ BŁĘDU (404 NOT FOUND)</div>
  <h2>Propagacja błędu braku produktu (ID: 999)</h2>
  <p class="subtitle">Serwis Magazynowy wykrywa kod 404 z Serwisu Produktów i zwraca spójny błąd 404 klientowi.</p>

  <div class="flow-box">
    <strong>Przebieg obsługi błędu:</strong>
    <span>Klient ──[GET /stock/999]──▶ Serwis Magazynowy ──[GET /products/999]──▶ Serwis Produktów [404 Not Found] ──▶ Zwrot 404 do Klienta</span>
  </div>

  <div style="height: 14px;"></div>

  <div class="terminal">
    <div class="terminal-bar">
      <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
      <div class="title">Klient REST (cURL) - Zapytanie o stan nieistniejącego produktu</div>
    </div>
    <div class="terminal-content">
      <div><span class="prompt">PS C:\Users\Mik&gt;</span> <span class="cmd">curl.exe -i http://localhost:8002/stock/999</span></div>
      <div style="margin-top: 10px;">
        <span class="status-404">HTTP/1.1 404 Not Found</span><br>
        <span class="header-name">date:</span> <span class="header-val">Fri, 14 Nov 2026 08:55:52 GMT</span><br>
        <span class="header-name">server:</span> <span class="header-val">uvicorn</span><br>
        <span class="header-name">content-length:</span> <span class="header-val">68</span><br>
        <span class="header-name">content-type:</span> <span class="header-val">application/json</span><br>
        <br>
        {<br>
        &nbsp;&nbsp;<span class="json-key">"detail"</span>: <span class="json-str">"Produkt o ID 999 nie istnieje w Serwisie Produktów."</span><br>
        }
      </div>
    </div>
  </div>

  <div class="terminal">
    <div class="terminal-bar">
      <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
      <div class="title">Weryfikacja bezpośrednia w Serwisie Produktów (Port 8001)</div>
    </div>
    <div class="terminal-content">
      <div><span class="prompt">PS C:\Users\Mik&gt;</span> <span class="cmd">curl.exe -i http://localhost:8001/products/999</span></div>
      <div style="margin-top: 10px;">
        <span class="status-404">HTTP/1.1 404 Not Found</span><br>
        <span class="header-name">content-type:</span> <span class="header-val">application/json</span><br>
        <br>
        {<br>
        &nbsp;&nbsp;<span class="json-key">"detail"</span>: <span class="json-str">"Produkt o ID 999 nie został znaleziony."</span><br>
        }
      </div>
    </div>
  </div>
</body>
</html>
"""

def generate_png_screenshot(html_content, output_png, width=1200, height=750):
    temp_html = output_png.replace(".png", "_temp.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        EDGE_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--window-size={width},{height}",
        f"--screenshot={output_png}",
        temp_html
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Wygenerowano zrzut ekranu: {output_png}")

def main():
    print("Rozpoczynanie generowania zrzutów ekranu...")
    p1 = os.path.join(SCREENSHOTS_DIR, "01_running_servers.png")
    p2 = os.path.join(SCREENSHOTS_DIR, "02_success_scenario.png")
    p3 = os.path.join(SCREENSHOTS_DIR, "03_error_scenario.png")

    generate_png_screenshot(HTML_SERVERS, p1, width=1200, height=650)
    generate_png_screenshot(HTML_SUCCESS, p2, width=1200, height=780)
    generate_png_screenshot(HTML_ERROR, p3, width=1200, height=780)
    print("Wszystkie zrzuty ekranu zostały pomyślnie wygenerowane w katalogu screenshots/!")

if __name__ == "__main__":
    main()
