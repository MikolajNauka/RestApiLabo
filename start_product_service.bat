@echo off
title Serwis Produktow (Port 8001)
echo Uruchamianie Serwisu Produktow na porcie 8001...
call .\venv\Scripts\activate.bat
python product_service\main.py
pause
