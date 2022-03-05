@echo off
:: extremely basic because i dont know how to batch.

python --version 3>NUL
if errorlevel 1 goto errorNoPython

py -m pip uninstall drop-mod -y
py setup.py install --user

goto:eof

:errorNoPython
echo.
echo Error^: Python not installed
