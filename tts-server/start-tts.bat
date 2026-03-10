@echo off
echo ========================================
echo   AlloFlow Edge TTS Server
echo   27 voices, 22+ languages
echo   OpenAI-compatible endpoint
echo ========================================
echo.
echo Starting on http://localhost:5500 ...
echo.
python "%~dp0edge_tts_server.py"
pause
