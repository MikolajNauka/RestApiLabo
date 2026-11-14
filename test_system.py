"""
Skrypt testujący poprawność działania obu mikroserwisów i komunikacji między nimi.
"""

import sys
import time
import requests

PRODUCT_SERVICE_URL = "http://127.0.0.1:8001"
STOCK_SERVICE_URL = "http://127.0.0.1:8002"

def print_separator(title=""):
    print("\n" + "=" * 65)
    if title:
        print(f" {title}")
        print("=" * 65)

def check_service_health():
    print("Sprawdzanie dostępności serwisów...")
    try:
        r1 = requests.get(f"{PRODUCT_SERVICE_URL}/", timeout=2)
        print(f" [+] Serwis Produktów (port 8001): OK (status {r1.status_code})")
    except Exception as e:
        print(f" [-] Serwis Produktów (port 8001): BŁĄD ({e})")
        return False

    try:
        r2 = requests.get(f"{STOCK_SERVICE_URL}/", timeout=2)
        print(f" [+] Serwis Magazynowy (port 8002): OK (status {r2.status_code})")
    except Exception as e:
        print(f" [-] Serwis Magazynowy (port 8002): BŁĄD ({e})")
        return False
    return True

def run_tests():
    print_separator("TESTY INTEGRACYJNE SYSTEMU ROZPROSZONEGO")
    
    if not check_service_health():
        print("\n[!] Upewnij się, że oba serwery są uruchomione przed uruchomieniem testów.")
        sys.exit(1)

    # Scenariusz 1: Pobranie istniejącego produktu z Serwisu Produktów
    print_separator("SCENARIUSZ 1A: GET /products/101 (Produkt istnieje)")
    res = requests.get(f"{PRODUCT_SERVICE_URL}/products/101")
    print(f"Żądanie: GET {PRODUCT_SERVICE_URL}/products/101")
    print(f"Status HTTP: {res.status_code}")
    print(f"Odpowiedź JSON: {res.json()}")
    assert res.status_code == 200, f"Oczekiwano 200, otrzymano {res.status_code}"
    assert res.json()["name"] == "Laptop Dell XPS 15"
    print(">>> WYNIK: SUKCES (200 OK)")

    # Scenariusz 1B: Sukces komunikacji między Serwisem Magazynowym a Serwisem Produktów
    print_separator("SCENARIUSZ 1B (KLUCZOWY): GET /stock/101 (Komunikacja między-serwisowa - SUKCES)")
    print("Opis: Serwis Magazynowy odpytuje Serwis Produktów o produkt 101, weryfikuje istnienie i zwraca stan.")
    res = requests.get(f"{STOCK_SERVICE_URL}/stock/101")
    print(f"Żądanie: GET {STOCK_SERVICE_URL}/stock/101")
    print(f"Status HTTP: {res.status_code}")
    print(f"Odpowiedź JSON: {res.json()}")
    assert res.status_code == 200, f"Oczekiwano 200, otrzymano {res.status_code}"
    assert res.json()["productId"] == 101
    assert res.json()["quantity"] == 15
    print(">>> WYNIK: SUKCES (200 OK)")

    # Scenariusz 2A: Próba pobrania nieistniejącego produktu z Serwisu Produktów
    print_separator("SCENARIUSZ 2A: GET /products/999 (Produkt nie istnieje)")
    res = requests.get(f"{PRODUCT_SERVICE_URL}/products/999")
    print(f"Żądanie: GET {PRODUCT_SERVICE_URL}/products/999")
    print(f"Status HTTP: {res.status_code}")
    print(f"Odpowiedź JSON: {res.json()}")
    assert res.status_code == 404, f"Oczekiwano 404, otrzymano {res.status_code}"
    print(">>> WYNIK: POPRAWNA OBSŁUGA BŁĘDU (404 Not Found)")

    # Scenariusz 2B: Próba pobrania stanu dla nieistniejącego produktu przez Serwis Magazynowy
    print_separator("SCENARIUSZ 2B (KLUCZOWY): GET /stock/999 (Propagacja błędu 404 z Serwisu Produktów)")
    print("Opis: Serwis Magazynowy pyta Serwis Produktów o produkt 999 -> otrzymuje 404 -> propaguje 404 do klienta.")
    res = requests.get(f"{STOCK_SERVICE_URL}/stock/999")
    print(f"Żądanie: GET {STOCK_SERVICE_URL}/stock/999")
    print(f"Status HTTP: {res.status_code}")
    print(f"Odpowiedź JSON: {res.json()}")
    assert res.status_code == 404, f"Oczekiwano 404, otrzymano {res.status_code}"
    print(">>> WYNIK: POPRAWNA PROPAGACJA BŁĘDU 404 (404 Not Found)")

    print_separator("WSZYSTKIE TESTY ZAKOŃCZONE POMYŚLNIE!")

if __name__ == "__main__":
    run_tests()
