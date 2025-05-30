@echo off
title SyntaxConnect Bot - Menu
color 01
cls

:: Arte ASCII estilosa

echo ============================================
echo       BEM-VINDO AO SYNTAX CONNECT BOT
echo ============================================
echo.
echo   [1] Iniciar o bot
echo   [0] Fechar
echo.
set /p escolha="Escolha uma opcao: "

if "%escolha%"=="1" goto iniciar
if "%escolha%"=="0" exit

echo.
echo Opcao invalida. Tente novamente.
pause
exit

:iniciar
cls
echo ============================================
echo           Iniciando o bot...
echo ============================================
cd /d "C:\Users\PARAFAL\Desktop\SyntaxConnect_Bot\app"
python bot.py
pause
exit
