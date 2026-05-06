@echo off
REM Samsung Seoul Hospital - Azure 배포 스크립트 (Windows)

setlocal enabledelayedexpansion

echo.
echo ============================================
echo Samsung Seoul Hospital - Azure 배포
echo ============================================
echo.

REM Azure CLI 로그인
echo [1/9] Azure CLI 로그인 중...
call az login
if errorlevel 1 goto error

REM 리소스 그룹 생성
echo.
echo [2/9] 리소스 그룹 생성 중...
call az group create --name samsung-rg --location koreacentral
if errorlevel 1 goto error

REM PostgreSQL 데이터베이스 생성
echo.
echo [3/9] PostgreSQL 데이터베이스 생성 중... (약 5-10분 소요)
call az postgres flexible-server create ^
  --resource-group samsung-rg ^
  --name samsung-db-server ^
  --location koreacentral ^
  --admin-user dbadmin ^
  --admin-password "Samsung2026@Secure!" ^
  --sku-name Standard_B1ms ^
  --tier Burstable ^
  --storage-size 32 ^
  --version 13
if errorlevel 1 goto error

REM 데이터베이스 생성
echo.
echo [4/9] hospitaldb 데이터베이스 생성 중...
call az postgres flexible-server db create ^
  --resource-group samsung-rg ^
  --server-name samsung-db-server ^
  --database-name hospitaldb
if errorlevel 1 goto error

REM 방화벽 규칙 설정
echo.
echo [5/9] 방화벽 규칙 설정 중...
call az postgres flexible-server firewall-rule create ^
  --resource-group samsung-rg ^
  --name samsung-db-server ^
  --rule-name AllowAllAzureIps ^
  --start-ip-address 0.0.0.0 ^
  --end-ip-address 255.255.255.255
if errorlevel 1 goto error

REM App Service 계획 생성
echo.
echo [6/9] App Service 계획 생성 중...
call az appservice plan create ^
  --name samsung-plan ^
  --resource-group samsung-rg ^
  --sku B1 ^
  --is-linux
if errorlevel 1 goto error

REM Web App 생성 및 배포
echo.
echo [7/9] Web App 생성 및 배포 중... (약 3-5분 소요)
call az webapp up ^
  --resource-group samsung-rg ^
  --name samsung-app ^
  --plan samsung-plan ^
  --runtime "python|3.11"
if errorlevel 1 goto error

REM 환경 변수 설정
echo.
echo [8/9] 환경 변수 설정 중...
call az webapp config appsettings set ^
  --resource-group samsung-rg ^
  --name samsung-app ^
  --settings ^
    ENVIRONMENT="production" ^
    SECRET_KEY="samsung-secret-key-2026" ^
    DATABASE_URL="postgresql://dbadmin:Samsung2026@Secure!@samsung-db-server.postgres.database.azure.com:5432/hospitaldb"
if errorlevel 1 goto error

REM HTTPS 설정
echo.
echo [9/9] HTTPS 전용 설정 중...
call az webapp config set ^
  --resource-group samsung-rg ^
  --name samsung-app ^
  --https-only true
if errorlevel 1 goto error

echo.
echo ============================================
echo 배포 완료!
echo ============================================
echo.
echo 🎉 축하합니다!
echo.
echo 배포된 URL: https://samsung-app.azurewebsites.net
echo.
echo 테스트 계정:
echo   - 사용자명: demo
echo   - 비밀번호: demo123
echo.

pause
exit /b 0

:error
echo.
echo 에러가 발생했습니다!
pause
exit /b 1
