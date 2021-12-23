@echo off
cmd /k "cd venv\Scripts & activate & cd .. & cd.. & python main.py"
venv\Scripts\activate.bat
pause
python main.py
pause