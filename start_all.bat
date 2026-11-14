@echo off
echo Uruchamianie obu mikroserwisow w oddzielnych oknach...
start "Serwis Produktow - Port 8001" cmd /k ".\venv\Scripts\activate.bat && python product_service\main.py"
start "Serwis Magazynowy - Port 8002" cmd /k ".\venv\Scripts\activate.bat && python stock_service\main.py"
echo Serwisy zostaly uruchomione!
echo Serwis Produktow:  http://127.0.0.1:8001/docs
echo Serwis Magazynowy: http://127.0.0.1:8002/docs
