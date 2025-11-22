@echo off
echo Setting up email notification environment variables
echo ================================================

set /p smtp_server="Enter SMTP server (e.g., smtp.gmail.com): "
set /p sender_email="Enter sender email address: "
set /p sender_password="Enter sender password (or app-specific password): "
set /p recipient_email="Enter recipient email address: "

setx SMTP_SERVER "%smtp_server%"
setx SENDER_EMAIL "%sender_email%"
setx SENDER_PASSWORD "%sender_password%"
setx RECIPIENT_EMAIL "%recipient_email%"

echo.
echo Environment variables have been set:
echo SMTP_SERVER=%smtp_server%
echo SENDER_EMAIL=%sender_email%
echo SENDER_PASSWORD=********
echo RECIPIENT_EMAIL=%recipient_email%
echo.
echo These variables will be available in new command prompt windows.
echo To use them in the current window, run:
echo set SMTP_SERVER=%smtp_server%
echo set SENDER_EMAIL=%sender_email%
echo set SENDER_PASSWORD=%sender_password%
echo set RECIPIENT_EMAIL=%recipient_email%
echo.
pause