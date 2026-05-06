# 🚀 즉시 배포 가이드

## ✅ samsung-app 폴더 구조

모든 파일이 `C:\Users\k-dae\OneDrive\문서\Workspaces\samsung-app\` 에 준비되었습니다.

```
samsung-app/
├── 📄 app.py                    (Flask 애플리케이션)
├── 📄 requirements.txt          (Python 패키지)
├── 📄 Dockerfile               (Docker 설정)
├── 📄 .env.example             (환경 변수 템플릿)
├── 📄 .gitignore               (Git 제외 파일)
├── 📄 deploy.bat               (Windows 배포 스크립트)
├── 📄 README.md                (프로젝트 설명)
├── 📄 DEPLOY_NOW.md            (이 파일)
└── 📁 templates/               (HTML 템플릿)
    ├── base.html               (기본 레이아웃)
    ├── login.html              (로그인 - Azure 푸터 포함)
    ├── signup.html             (회원가입)
    ├── board.html              (게시판)
    ├── post.html               (게시물)
    ├── new_post.html           (새 글 작성)
    ├── hospital.html           (병원 정보)
    └── developer.html          (개발자 프로필)
```

## 🎯 Azure에 즉시 배포하기

### 방법 1: 자동 배포 스크립트 (가장 간단)

**Windows PowerShell에서** (관리자 권한):
```powershell
cd C:\Users\k-dae\OneDrive\문서\Workspaces\samsung-app
.\deploy.bat
```

이 스크립트가 자동으로 다음을 수행합니다:
1. ✅ Azure 로그인
2. ✅ 리소스 그룹 생성
3. ✅ PostgreSQL 데이터베이스 생성 (5-10분)
4. ✅ App Service 생성 및 배포 (3-5분)
5. ✅ 환경 변수 설정
6. ✅ HTTPS 활성화

**총 소요 시간: 약 20-30분**

---

## 📋 수동 배포 (한 줄씩)

Azure CLI를 이용한 수동 배포:

```bash
# 1. Azure 로그인
az login

# 2. 리소스 그룹
az group create --name samsung-rg --location koreacentral

# 3. PostgreSQL (5-10분 소요)
az postgres flexible-server create ^
  --resource-group samsung-rg ^
  --name samsung-db-server ^
  --location koreacentral ^
  --admin-user dbadmin ^
  --admin-password "Samsung2026@Secure!" ^
  --sku-name Standard_B1ms ^
  --tier Burstable ^
  --storage-size 32 ^
  --version 13

# 4. 데이터베이스
az postgres flexible-server db create ^
  --resource-group samsung-rg ^
  --server-name samsung-db-server ^
  --database-name hospitaldb

# 5. 방화벽
az postgres flexible-server firewall-rule create ^
  --resource-group samsung-rg ^
  --name samsung-db-server ^
  --rule-name AllowAllAzureIps ^
  --start-ip-address 0.0.0.0 ^
  --end-ip-address 255.255.255.255

# 6. App Service 계획
az appservice plan create ^
  --name samsung-plan ^
  --resource-group samsung-rg ^
  --sku B1 ^
  --is-linux

# 7. Web App 배포 (3-5분 소요)
cd C:\Users\k-dae\OneDrive\문서\Workspaces\samsung-app
az webapp up ^
  --resource-group samsung-rg ^
  --name samsung-app ^
  --plan samsung-plan ^
  --runtime "python|3.11"

# 8. 환경 변수
az webapp config appsettings set ^
  --resource-group samsung-rg ^
  --name samsung-app ^
  --settings ^
    ENVIRONMENT="production" ^
    SECRET_KEY="samsung-secret-key-2026" ^
    DATABASE_URL="postgresql://dbadmin:Samsung2026@Secure!@samsung-db-server.postgres.database.azure.com:5432/hospitaldb"

# 9. HTTPS 활성화
az webapp config set ^
  --resource-group samsung-rg ^
  --name samsung-app ^
  --https-only true
```

---

## 🌐 배포 완료 후

### 접속 URL
```
https://samsung-app.azurewebsites.net
```

### 로그인
- **사용자명**: demo
- **비밀번호**: demo123

### 주요 페이지
- 로그인: https://samsung-app.azurewebsites.net/login
- 게시판: https://samsung-app.azurewebsites.net/board
- 병원정보: https://samsung-app.azurewebsites.net/hospital
- 개발자: https://samsung-app.azurewebsites.net/developer

---

## 🔍 배포 확인

### 실시간 로그 보기
```bash
az webapp log tail --resource-group samsung-rg --name samsung-app
```

### 배포 상태 확인
```bash
az webapp deployment list --resource-group samsung-rg --name samsung-app
```

### App Service 재시작
```bash
az webapp restart --resource-group samsung-rg --name samsung-app
```

---

## 📊 배포 정보

| 항목 | 값 |
|------|-----|
| **App Name** | samsung-app |
| **URL** | https://samsung-app.azurewebsites.net |
| **Resource Group** | samsung-rg |
| **Location** | Korea Central |
| **Pricing** | B1 Standard (~$12/월) |
| **Database** | PostgreSQL 13 (~$30/월) |
| **총 비용** | ~$42/월 |

---

## ✨ 포함된 기능

✅ 사용자 인증 (회원가입/로그인)
✅ 토론 게시판 (카테고리, 검색)
✅ 게시물 작성/조회/삭제
✅ 댓글 기능
✅ 병원 정보 페이지
✅ 개발자 프로필 페이지
✅ HTTPS/TLS 암호화
✅ Azure 클라우드 배포
✅ PostgreSQL 데이터베이스
✅ 반응형 모바일 디자인
✅ DaeseokKim 저작권 표시
✅ Azure 인프라 정보 푸터

---

## 🐛 문제 해결

### 500 에러
```bash
az webapp log tail --resource-group samsung-rg --name samsung-app --provider AppServiceApplicationLogs
```

### 데이터베이스 연결 실패
```bash
# 방화벽 규칙 재설정
az postgres flexible-server firewall-rule delete --resource-group samsung-rg --name samsung-db-server --rule-name AllowAllAzureIps

az postgres flexible-server firewall-rule create --resource-group samsung-rg --name samsung-db-server --rule-name AllowAllAzureIps --start-ip-address 0.0.0.0 --end-ip-address 255.255.255.255
```

### 배포 실패 시
1. Azure CLI 버전 확인: `az --version`
2. 로그인 재확인: `az login`
3. 리소스 상태 확인: `az group show --name samsung-rg`

---

## 🎉 완료!

이제 `samsung-app` 폴더의 모든 파일이 준비되었습니다.

**다음 단계:**
1. PowerShell 또는 Bash에서 `deploy.bat` 실행
2. 약 20-30분 대기
3. https://samsung-app.azurewebsites.net 접속
4. 테스트 계정으로 로그인

**축하합니다! Samsung Seoul Hospital 애플리케이션이 Azure에 배포됩니다!** 🚀
