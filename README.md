# Samsung Seoul Hospital - 토론 플랫폼

Flask 기반 웹 애플리케이션으로, Samsung Seoul Hospital의 직원과 방문객을 위한 토론 게시판, 병원 정보, 개발자 프로필을 제공합니다.

## 🚀 빠른 배포

### Windows
```bash
cd C:\Users\k-dae\OneDrive\문서\Workspaces\samsung-app
deploy.bat
```

### macOS/Linux
```bash
chmod +x ~/OneDrive/문서/Workspaces/samsung-app/deploy.sh
~/OneDrive/문서/Workspaces/samsung-app/deploy.sh
```

## 📦 폴더 구조

```
samsung-app/
├── app.py                 # Flask 메인 애플리케이션
├── requirements.txt       # Python 의존성
├── Dockerfile            # Docker 설정
├── .env.example          # 환경 변수 예시
├── .gitignore           # Git 제외 파일
├── deploy.bat           # Windows 배포 스크립트
├── deploy.sh            # Linux/Mac 배포 스크립트
├── README.md            # 이 파일
└── templates/           # HTML 템플릿
    ├── base.html
    ├── login.html
    ├── signup.html
    ├── board.html
    ├── post.html
    ├── new_post.html
    ├── hospital.html
    └── developer.html
```

## 🌟 주요 기능

- ✅ 사용자 인증 (회원가입/로그인)
- ✅ 토론 게시판 (카테고리, 검색)
- ✅ 게시물 작성/조회/댓글
- ✅ 병원 정보 페이지
- ✅ 개발자 프로필
- ✅ HTTPS/TLS 보안
- ✅ Azure 클라우드 배포

## 🔐 테스트 계정

- **사용자명**: demo
- **비밀번호**: demo123

## 📊 기술 스택

- **Backend**: Flask, SQLAlchemy
- **Database**: PostgreSQL, SQLite
- **Frontend**: HTML5, CSS3
- **Cloud**: Microsoft Azure
- **Container**: Docker

## 🌐 배포 후 접속

```
https://samsung-app.azurewebsites.net
```

## 📝 환경 변수

`.env` 파일:
```
SECRET_KEY=samsung-secret-key-2026
ENVIRONMENT=development
DATABASE_URL=sqlite:///hospital.db
```

## 💻 로컬 실행

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## 👨‍💻 개발자 정보

- **이름**: 김대석 (DaeseokKim)
- **부서**: 첨단인프라운영팀
- **이메일**: kds5192@gmail.com

Copyright © 2026 DaeseokKim. All Rights Reserved.
