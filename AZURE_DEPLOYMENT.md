# Azure Container Instances 배포 가이드

## 📋 필수 요소
- Azure 구독 (계정명, 구독ID)
- Docker Desktop 설치
- Azure CLI 설치

---

## 🔧 Step 1: Azure CLI 설치 및 로그인

### Windows PowerShell (관리자)에서:
```powershell
# Azure CLI 설치 (이미 설치된 경우 스킵)
winget install Microsoft.AzureCLI

# Azure 로그인
az login
```

---

## 🐳 Step 2: Docker 이미지 빌드

### 로컬에서 먼저 테스트:
```bash
cd C:\Users\k-dae\OneDrive\문서\Workspaces\samsung_app

# Docker 이미지 빌드
docker build -t samsung-app:latest .

# 로컬 테스트 (선택사항)
docker run -p 5000:5000 samsung-app:latest
# 브라우저: http://localhost:5000
```

---

## ☁️ Step 3: Azure Container Registry에 Push

### 1. Container Registry 생성 (처음 한 번만)
```bash
# 리소스 그룹 생성
az group create --name samsung-rg --location koreacentral

# Container Registry 생성
az acr create --resource-group samsung-rg --name samsungapp --sku Basic
```

### 2. 로그인 및 이미지 Push
```bash
# ACR 로그인
az acr login --name samsungapp

# 이미지 태그 지정
docker tag samsung-app:latest samsungapp.azurecr.io/samsung-app:latest

# 이미지 Push
docker push samsungapp.azurecr.io/samsung-app:latest

# 확인
az acr repository list --name samsungapp
```

---

## 🚀 Step 4: Container Instances 배포

### 방법 A: 명령어로 배포 (추천)
```bash
az container create \
  --resource-group samsung-rg \
  --name samsung-app-instance \
  --image samsungapp.azurecr.io/samsung-app:latest \
  --registry-login-server samsungapp.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --cpu 1 \
  --memory 1 \
  --ports 5000 \
  --environment-variables \
    FLASK_ENV=production \
    DATABASE_URL=postgresql+pg8000://postgres:kds0914@your-postgres-host:5432/samsung_app \
  --protocol TCP
```

**username/password 확인:**
```bash
az acr credential show --name samsungapp
```

---

## 📍 Step 5: 배포된 앱 접속

```bash
# 컨테이너 상태 확인
az container show --resource-group samsung-rg --name samsung-app-instance

# 공용 IP 확인
az container list --resource-group samsung-rg --output table
```

**브라우저에서:**
```
http://<공용-IP>:5000
```

---

## 🗄️ PostgreSQL 연결 (Azure Database for PostgreSQL)

### 1. PostgreSQL 서버 생성 (선택사항)
```bash
az postgres server create \
  --resource-group samsung-rg \
  --name samsung-postgres \
  --admin-user postgres \
  --admin-password kds0914 \
  --sku-name B_Gen5_1 \
  --storage-size 51200 \
  --location koreacentral
```

### 2. 방화벽 규칙 추가
```bash
az postgres server firewall-rule create \
  --resource-group samsung-rg \
  --server-name samsung-postgres \
  --name AllowAllIps \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 255.255.255.255
```

### 3. 연결 문자열
```
postgresql+pg8000://postgres:kds0914@samsung-postgres.postgres.database.azure.com:5432/samsung_app
```

---

## ❌ 문제 해결

### 컨테이너가 실행되지 않음
```bash
az container logs --resource-group samsung-rg --name samsung-app-instance
```

### 레지스트리에 이미지 없음
```bash
docker push samsungapp.azurecr.io/samsung-app:latest
```

### 데이터베이스 연결 실패
- `.env` 파일의 `DATABASE_URL` 확인
- Azure PostgreSQL 방화벽 규칙 확인

---

## 🧹 정리 (선택사항)

모든 리소스 삭제:
```bash
az group delete --name samsung-rg --yes
```

---

## 📞 추가 지원
- [Azure CLI 문서](https://docs.microsoft.com/cli/azure/)
- [Azure Container Instances](https://docs.microsoft.com/azure/container-instances/)
