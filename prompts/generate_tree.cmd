@echo off
.\tools\tree.exe -I ".conda" -P "*.py" -f ../ > structure.txt