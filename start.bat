@echo off
cmd /k "cd env\Scripts & activate & cd .. & cd.. & python main.py"
venv\Scripts\activate.bat
pause
python main.py
pause