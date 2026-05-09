@echo off
title Alenia Studios - Empaquetador Porter v3.0
setlocal

echo 1. Preparando la fabrica en C:\AleniaBuild...
if exist C:\AleniaBuild rd /s /q C:\AleniaBuild
mkdir C:\AleniaBuild

echo 2. Copiando materiales desde D:\tool\porter...
copy "D:\tool\porter\main.py" "C:\AleniaBuild\"
copy "D:\tool\porter\porter_logic.py" "C:\AleniaBuild\"
copy "D:\tool\porter\locales.json" "C:\AleniaBuild\"
copy "D:\tool\porter\logo.ico" "C:\AleniaBuild\"
copy "D:\tool\porter\ffmpeg.EXE" "C:\AleniaBuild\"
copy "D:\tool\porter\ffprobe.EXE" "C:\AleniaBuild\"

echo 3. Entrando al taller seguro en C:...
cd /d C:\AleniaBuild

echo 4. Compilando Alenia Porter v3.0 (Estructura Limpia)...
pyinstaller --noconsole --onedir --clean --noupx --contents-directory internal --add-data "logo.ico;." --add-data "locales.json;." --add-data "ffmpeg.EXE;." --add-data "ffprobe.EXE;." --icon=logo.ico --name="AleniaPorter" main.py
echo.
echo 5. Moviendo la carpeta lista a D:\tool\porter...
if exist "D:\tool\porter\AleniaPorter_v3.0" rd /s /q "D:\tool\porter\AleniaPorter_v3.0"
xcopy "C:\AleniaBuild\dist\AleniaPorter" "D:\tool\porter\AleniaPorter_v3.0" /E /I /H /Y

echo 6. Limpiando el taller temporal en C:...
cd /d D:\tool\porter
rd /s /q C:\AleniaBuild

echo.
echo =======================================================
echo ¡ESTRUCTURA PORTER V3.0 CREADA!
echo Revisa: D:\tool\porter\AleniaPorter_v3.0\
echo =======================================================
pause
endlocal