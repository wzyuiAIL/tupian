@echo off
title Web Server
cd assets
echo Starting server on port 8080...
echo Open: http://localhost:8080/web_sdk_index.html
echo.
echo Press Ctrl+C to stop
echo.
python -m http.server 8080
pause