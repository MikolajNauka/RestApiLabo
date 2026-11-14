@echo off
title Serwis Magazynowy (Port 8002)
echo Uruchamianie Serwisu Magazynowego na porcie 8002...
call .\venv\Scripts\activate.bat
python stock_service\main.py
pause
