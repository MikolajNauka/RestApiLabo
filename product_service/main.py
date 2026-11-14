"""
Serwis Produktów (Product Service)
Port: 8001
Zarządza informacjami o produktach (katalog produktów).
"""

from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Serwis Produktów (Product Service)",
    description="Mikroserwis zarządzający bazą produktów w systemie rozproszonym.",
    version="1.0.0"
)

# Model reprezentujący pojedynczy produkt
class Product(BaseModel):
    id: int
    name: str
    price: float

# Baza danych w pamięci (mock)
PRODUCTS_DB: Dict[int, Product] = {
    101: Product(id=101, name="Laptop Dell XPS 15", price=7499.99),
    102: Product(id=102, name="Klawiatura mechaniczna Keychron K2", price=429.00),
    103: Product(id=103, name="Mysz bezprzewodowa Logitech MX Master 3S", price=499.00),
    104: Product(id=104, name="Monitor Dell UltraSharp 27\"", price=1899.00),
    105: Product(id=105, name="Słuchawki bezprzewodowe Sony WH-1000XM5", price=1399.00),
}


@app.get("/", tags=["Informacje"])
def read_root():
    """Podstawowe informacje o serwisie produktów."""
    return {
        "service": "Serwis Produktów",
        "status": "działa poprawnie",
        "port": 8001,
        "endpoints": {
            "pobierz_produkt": "GET /products/{id}",
            "wszystkie_produkty": "GET /products",
            "dokumentacja_swagger": "GET /docs"
        }
    }


@app.get("/products", response_model=List[Product], tags=["Produkty"])
def get_all_products():
    """Zwraca listę wszystkich dostępnych produktów."""
    return list(PRODUCTS_DB.values())


@app.get(
    "/products/{product_id}",
    response_model=Product,
    tags=["Produkty"],
    responses={
        200: {"description": "Pomyślnie znaleziono produkt."},
        404: {"description": "Produkt o podanym ID nie istnieje."}
    }
)
def get_product(product_id: int):
    """
    Zwraca szczegółowe dane produktu o podanym ID.
    W przypadku braku produktu zwraca błąd HTTP 404 Not Found.
    """
    product = PRODUCTS_DB.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produkt o ID {product_id} nie został znaleziony."
        )
    return product


if __name__ == "__main__":
    print("Uruchamianie Serwisu Produktów na porcie 8001...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
