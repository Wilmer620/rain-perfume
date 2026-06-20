@echo off
cd /d "C:\Users\Ara\rain-website"

echo [%date% %time%] Starting RAIN server... >> startup.log

:: Start Node.js server
start "RAIN-Server" /MIN node "C:\Users\Ara\rain-website\server.js"

:: Wait for server
timeout /t 4 /nobreak > nul

:: Start ngrok tunnel
start "RAIN-Ngrok" /MIN "C:\Users\Ara\AppData\Local\Microsoft\WinGet\Packages\Ngrok.Ngrok_Microsoft.Winget.Source_8wekyb3d8bbwe\ngrok.exe" http 3000

echo [%date% %time%] RAIN startup complete >> startup.log

:: Extract URL after ngrok starts
timeout /t 6 /nobreak > nul
curl -s http://localhost:4040/api/tunnels > tunnel.json 2>nul
for /f "tokens=*" %%a in ('powershell -Command "(Get-Content tunnel.json | ConvertFrom-Json).tunnels[0].public_url" 2^>nul') do (
  echo [%date% %time%] Tunnel: %%a >> startup.log
)
exit
