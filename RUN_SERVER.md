# Samsung App - 서버 실행 가이드

## 1️⃣ 환경 설정 (처음 한 번만)

```bash
# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows CMD:
venv\Scripts\activate

# Windows PowerShell:
venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt
```

## 2️⃣ PostgreSQL 데이터베이스 생성

```sql
-- PostgreSQL 접속
psql -U postgres

-- 데이터베이스 생성
CREATE DATABASE samsung_app;

-- 확인
\l
```

## 3️⃣ 환경 변수 확인 (.env 파일)

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:kds0914@localhost:5432/samsung_app
FLASK_ENV=development
FLASK_DEBUG=True
```

**주의:** `.env`의 PostgreSQL 비밀번호(`kds0914`)가 실제 비밀번호와 일치하는지 확인하세요!

## 4️⃣ 서버 실행

```bash
# 가상환경이 활성화된 상태에서
python app.py
```

또는 VS Code에서:
- **Ctrl+`** (백틱) → Terminal 열기
- `python app.py` 입력 후 Enter

## 5️⃣ 접속 확인

브라우저에서 열기:
```
http://localhost:5000
```

**로그인 페이지가 나타나면 성공!**

## 📝 테스트 계정 생성 (선택)

1. http://localhost:5000 접속
2. "회원가입" 클릭
3. 다음 정보 입력:
   - 사용자명: `testuser`
   - 이메일: `test@example.com`
   - 비밀번호: `password123`
4. 로그인 후 대시보드 접근 확인

## ❌ 문제 해결

### "Connection refused" 에러
→ PostgreSQL 서비스가 실행 중인지 확인
→ `kds0914` 비밀번호가 맞는지 확인

### "ModuleNotFoundError" 에러
→ 가상환경이 활성화되어 있는지 확인
→ `pip install -r requirements.txt` 다시 실행

### 포트 5000 이미 사용 중
→ `app.py` 마지막 줄의 port를 5001로 변경하고 재실행
