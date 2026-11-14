"""
Skrypt pomocniczy do równoległego uruchomienia obu serwisów w osobnych wątkach/procesach.
"""

import multiprocessing
import time
import uvicorn
from product_service.main import app as product_app
from stock_service.main import app as stock_app

def start_product_service():
    print("[Serwis Produktów] Start na http://127.0.0.1:8001")
    uvicorn.run(product_app, host="127.0.0.1", port=8001, log_level="info")

def start_stock_service():
    print("[Serwis Magazynowy] Start na http://127.0.0.1:8002")
    uvicorn.run(stock_app, host="127.0.0.1", port=8002, log_level="info")

if __name__ == "__main__":
    print("=" * 60)
    print(" URUCHAMIANIE SYSTEMU ROZPROSZONEGO (2 MIKROSERWISY)")
    print("  1. Serwis Produktów:  http://127.0.0.1:8001 (Docs: /docs)")
    print("  2. Serwis Magazynowy: http://127.0.0.1:8002 (Docs: /docs)")
    print(" Naciśnij CTRL+C, aby zatrzymać oba serwisy.")
    print("=" * 60)

    p1 = multiprocessing.Process(target=start_product_service)
    p2 = multiprocessing.Process(target=start_stock_service)

    p1.start()
    p2.start()

    try:
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        print("\nZatrzymywanie serwisów...")
        p1.terminate()
        p2.terminate()
        p1.join()
        p2.join()
        print("Oba serwisy zostały zatrzymane.")
