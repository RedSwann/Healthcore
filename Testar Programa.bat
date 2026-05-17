@echo off
cd /d %~dp0
set PYTHONPATH=src

echo Rodando testes...

py -m unittest discover -v tests

pause