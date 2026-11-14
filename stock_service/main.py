"""
Serwis Magazynowy (Stock Service)
Port: 8002
Zarządza stanem magazynowym produktów i komunikuje się z Serwisem Produktów przez REST API.
"""

from typing import Dict, Optional
import os
import requests
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Serwis Magazynowy (Stock Service)",
    description="Mikroserwis zarządzający stanami magazynowymi weryfikujący istnienie produktów w Serwisie Produktów.",
    version="1.0.0"
)

# Adres URL Serwisu Produktów (możliwość konfiguracji przez zmienną środowiskową)
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://127.0.0.1:8001")

# Model reprezentujący stan magazynowy
class StockResponse(BaseModel):
    productId: int
    quantity: int

# Baza stanów magazynowych w pamięci (mock)
STOCK_DB: Dict[int, int] = {
    101: 15,
    102: 42,
    103: 28,
    104: 8,
    105: 0,
}


@app.get("/", tags=["Informacje"])
def read_root():
    """Podstawowe informacje o serwisie magazynowym."""
    return {
        "service": "Serwis Magazynowy",
        "status": "działa poprawnie",
        "port": 8002,
        "product_service_url": PRODUCT_SERVICE_URL,
        "endpoints": {
            "pobierz_stan": "GET /stock/{productId}",
            "dokumentacja_swagger": "GET /docs"
        }
    }


@app.get(
    "/stock/{product_id}",
    response_model=StockResponse,
    tags=["Magazyn"],
    responses={
        200: {"description": "Pomyślnie pobrano stan magazynowy produktu."},
        404: {"description": "Produkt nie istnieje w Serwisie Produktów."},
        503: {"description": "Serwis Produktów jest niedostępny."}
    }
)
def get_stock(product_id: int):
    """
    Pobiera stan magazynowy dla danego produktu.
    Kluczowa logika:
    1. Wykonuje synchroniczne zapytanie HTTP GET do Serwisu Produktów (/products/{id}).
    2. Jeśli Serwis Produktów zwróci 200 OK -> zwraca stan magazynowy.
    3. Jeśli Serwis Produktów zwróci 404 Not Found -> zwraca 404 informując o braku produktu.
    4. Jeśli wystąpi błąd połączenia -> zwraca błąd 503 Service Unavailable.
    """
    # 1. Sprawdzenie istnienia produktu w Serwisie Produktów
    try:
        response = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}",
            timeout=3.0
        )
    except requests.exceptions.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Błąd komunikacji z Serwisem Produktów ({PRODUCT_SERVICE_URL}): {str(exc)}"
        )

    # 2. Obsługa odpowiedzi 404 z Serwisu Produktów
    if response.status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produkt o ID {product_id} nie istnieje w Serwisie Produktów."
        )

    # 3. Obsługa ewentualnego innego kodu błędu z Serwisu Produktów
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Serwis Produktów zwrócił nieoczekiwany status HTTP: {response.status_code}"
        )

    # 4. Produkt istnieje – pobranie stanu magazynowego z lokalnej bazy (lub domyślnie 0)
    quantity = STOCK_DB.get(product_id, 0)

    return StockResponse(productId=product_id, quantity=quantity)


if __name__ == "__main__":
    print("Uruchamianie Serwisu Magazynowego na porcie 8002...")
    uvicorn.run(app, host="127.0.0.1", port=8002)
